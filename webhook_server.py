import os
import smtplib
import hmac
import hashlib
from email.mime.text import MIMEText
from fastapi import FastAPI, Request, HTTPException
import stripe

app = FastAPI()

STRIPE_WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET", "")
MAIL_SENDER = os.getenv("RP_MAIL_SENDER", "ops@rp-sec.com")
MAIL_PASSWORD = os.getenv("RP_MAIL_PASSWD", "")
SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))

SECRET_SALT = b"RP_SEC_STEALTH_V9_SALT"

def issue_license_key(customer_email: str) -> str:
    seed = hashlib.sha256(customer_email.encode()).hexdigest()[:8].upper()
    payload = f"RPSEC-{seed}".encode()
    sig = hmac.new(SECRET_SALT, payload, hashlib.sha256).hexdigest()[:12].upper()
    return f"RPSEC-{seed}-{sig}"

def send_license_email(to_email: str, license_key: str):
    msg = MIMEText(f"""平素よりRP Stealth Securityをご利用いただき誠にありがとうございます。

商用ライセンスのご購入・サブスクリプション登録が完了いたしました。
貴社環境でご利用いただける暗号化商用ライセンスキーを下記に発行いたしました。

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
【発行ライセンス情報】
プラン: RP Stealth Security - Commercial License (月額 ¥49,800)
ライセンスキー: {license_key}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

■ 初期設定方法
FastAPI / ASGI等のミドルウェア初期化パラメータに本キーを設定してください。

    app.add_middleware(
        StealthSecurityMiddleware,
        license_key="{license_key}",
        reflection_sink=True,
        chrono_storage=True
    )

ご不明な点や導入に関する技術サポートは本メール宛（ops@rp-sec.com）にお問い合わせください。

RP Security Operations
billing@rp-sec.com
""")
    msg["Subject"] = "【RP Stealth Security】商用ライセンスキー発行完了のご案内"
    msg["From"] = MAIL_SENDER
    msg["To"] = to_email

    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
        server.starttls()
        server.login(MAIL_SENDER, MAIL_PASSWORD)
        server.send_message(msg)

@app.post("/api/stripe-webhook")
async def handle_stripe_webhook(request: Request):
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, STRIPE_WEBHOOK_SECRET
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        # session を辞書型に変換してから安全に取得
        session_dict = session.to_dict() if hasattr(session, "to_dict") else dict(session)
        customer_email = (session_dict.get("customer_details") or {}).get("email") or session_dict.get("customer_email")
        if customer_email:
            key = issue_license_key(customer_email)
            send_license_email(customer_email, key)

    return {"status": "success"}
