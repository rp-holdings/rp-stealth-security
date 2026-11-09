import os
import uuid
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from fastapi import FastAPI, Request, HTTPException
import stripe

app = FastAPI(title="RP Stealth Security License Server")

# Stripe署名シークレット（環境変数から取得、未設定時はダミー）
STRIPE_WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET", "whsec_YOUR_WEBHOOK_SIGNING_SECRET")

# メール設定（環境変数またはデフォルト値）
SMTP_HOST = os.getenv("SMTP_HOST", "localhost")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USER = os.getenv("SMTP_USER", "")
SMTP_PASS = os.getenv("SMTP_PASS", "")
FROM_EMAIL = os.getenv("FROM_EMAIL", "noreply@rp-sec.com")


def issue_license_key(customer_email: str) -> str:
    """ライセンスキーを生成してログに記録"""
    raw_uuid = str(uuid.uuid4()).upper()
    license_key = f"RP9-{raw_uuid[:8]}-{raw_uuid[9:13]}-{raw_uuid[14:18]}"
    print("\n==================================================")
    print(f"[LICENSE ISSUED] Customer: {customer_email}")
    print(f"[LICENSE KEY]    {license_key}")
    print("==================================================\n")
    return license_key


def send_license_email(customer_email: str, license_key: str):
    """ライセンスキー案内メールを送信（ローカル検証時は送信不能でも即時継続）"""
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

    # SMTP接続先未設定またはローカルテスト時はタイムアウトを防ぐため即座にスキップ
    if SMTP_HOST in ("localhost", "127.0.0.1", "") and not SMTP_USER:
        print(f"[MAIL NOTICE] Local test environment detected. Mock mail generated for: {customer_email}")
        return

    try:
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=3) as server:
            if SMTP_USER and SMTP_PASS:
                server.starttls()
                server.login(SMTP_USER, SMTP_PASS)
            server.send_message(msg)
            print(f"[MAIL] Sent license email to {customer_email}")
    except Exception as e:
        print(f"[MAIL WARNING] Could not deliver email via SMTP: {e}")


@app.get("/")
def health_check():
    return {"status": "ok", "service": "RP Stealth Security Webhook Server"}


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

        # StripeObject から辞書型へ変換
        session_dict = session.to_dict() if hasattr(session, "to_dict") else dict(session)

        # 顧客メールアドレスの抽出
        customer_email = (
            (session_dict.get("customer_details") or {}).get("email")
            or session_dict.get("customer_email")
        )

        if customer_email:
            key = issue_license_key(customer_email)
            send_license_email(customer_email, key)

    return {"status": "success"}
