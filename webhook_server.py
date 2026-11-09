"""
RP Stealth Security V9 - Production License Automation Webhook Server
Copyright (c) 2026 RP LLC. All rights reserved.
"""

import os
import sys
import secrets
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from fastapi import FastAPI, Request, HTTPException
import stripe

from rp_stealth_security.license_validator import LicenseValidator

app = FastAPI(
    title="RP Stealth Security V9 - License Service",
    docs_url=None,
    redoc_url=None
)

# 署名シークレット
STRIPE_WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET")
if not STRIPE_WEBHOOK_SECRET or STRIPE_WEBHOOK_SECRET.startswith("whsec_YOUR"):
    print("[FATAL SECURITY ERROR] STRIPE_WEBHOOK_SECRET is not configured. Server refused to start.", file=sys.stderr)
    sys.exit(1)

# SMTP設定
SMTP_HOST = os.getenv("SMTP_HOST", "localhost")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USER = os.getenv("SMTP_USER", "")
SMTP_PASS = os.getenv("SMTP_PASS", "")
FROM_EMAIL = os.getenv("FROM_EMAIL", "noreply@rp-sec.com")

# 冪等性管理
PROCESSED_EVENT_IDS = set()


def issue_cryptographic_license_key(customer_email: str) -> str:
    """CSPRNG (secrets) による128ビットエントロピーの暗号学的ライセンスキー発行"""
    p1 = secrets.token_hex(4).upper()
    p2 = secrets.token_hex(4).upper()
    p3 = secrets.token_hex(4).upper()
    p4 = secrets.token_hex(4).upper()
    license_key = f"RP9-{p1}-{p2}-{p3}-{p4}"

    # 自己整合性検証
    if not LicenseValidator.validate_format(license_key):
        raise ValueError("Generated key failed format validation.")

    print("\n" + "=" * 50)
    print(f"[SECURITY AUDIT] License Key Issued Successfully")
    print(f"Customer:    {customer_email}")
    print(f"License Key: {license_key}")
    print("=" * 50 + "\n")
    return license_key


def send_license_email(customer_email: str, license_key: str):
    """案内メール送信（ノンブロッキングフェイルセーフ）"""
    subject = "【RP Stealth Security V9】ライセンスキー発行のご案内"
    body = f"""この度は「RP Stealth Security V9」をご購入いただき誠にありがとうございます。

お客様のライセンスキーを発行いたしました。
--------------------------------------------------
ライセンスキー: {license_key}
対象アカウント: {customer_email}
--------------------------------------------------

本キーを製品の認証画面または設定ファイルに入力してご利用を開始してください。

合同会社RP
サポート: support@rp-sec.com
"""
    msg = MIMEMultipart()
    msg["From"] = FROM_EMAIL
    msg["To"] = customer_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain", "utf-8"))

    if SMTP_HOST in ("localhost", "127.0.0.1", "") and not SMTP_USER:
        print(f"[MAIL NOTICE] Local test environment detected. Mock mail issued for: {customer_email}")
        return

    try:
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=5) as server:
            if SMTP_USER and SMTP_PASS:
                server.starttls()
                server.login(SMTP_USER, SMTP_PASS)
            server.send_message(msg)
            print(f"[MAIL SUCCESS] Dispatched to {customer_email}")
    except Exception as e:
        print(f"[MAIL FAILURE] Delivery failed: {e}", file=sys.stderr)


@app.get("/healthz")
def health_check():
    return {"status": "ok"}


@app.post("/api/stripe-webhook")
async def handle_stripe_webhook(request: Request):
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")

    if not sig_header:
        raise HTTPException(status_code=400, detail="Missing Stripe-Signature header")

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, STRIPE_WEBHOOK_SECRET
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Signature verification failed: {e}")

    event_id = event.get("id")

    if event_id in PROCESSED_EVENT_IDS:
        print(f"[WEBHOOK IDEMPOTENT] Duplicate event {event_id} ignored.")
        return {"status": "already_processed"}

    if event.get("type") == "checkout.session.completed":
        session = event.get("data", {}).get("object", {})
        session_dict = session.to_dict() if hasattr(session, "to_dict") else dict(session)

        payment_status = session_dict.get("payment_status")
        if payment_status != "paid":
            print(f"[WEBHOOK DEFERRED] Payment status is '{payment_status}'. License generation deferred.")
            return {"status": "deferred_unpaid"}

        customer_email = (
            (session_dict.get("customer_details") or {}).get("email")
            or session_dict.get("customer_email")
        )

        if customer_email:
            key = issue_cryptographic_license_key(customer_email)
            send_license_email(customer_email, key)
            PROCESSED_EVENT_IDS.add(event_id)
        else:
            print("[WEBHOOK WARN] checkout.session.completed event has no customer email.")

    return {"status": "success"}
