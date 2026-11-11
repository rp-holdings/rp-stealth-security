import os
import secrets
import stripe
import requests
from fastapi import FastAPI, Request, HTTPException, Header
from fastapi.responses import JSONResponse

app = FastAPI(title="RP Stealth License Delivery Webhook")

STRIPE_SECRET_KEY = os.environ.get("STRIPE_SECRET_KEY", "")
STRIPE_WEBHOOK_SECRET = os.environ.get("STRIPE_WEBHOOK_SECRET", "")
RESEND_API_KEY = os.environ.get("RESEND_API_KEY", "")
MAIL_FROM = os.environ.get("MAIL_FROM", "support@rp-sec.com")

stripe.api_key = STRIPE_SECRET_KEY

def generate_secure_license_key(customer_email: str) -> str:
    token = secrets.token_hex(16).upper()
    parts = [token[i:i+8] for i in range(0, 32, 8)]
    return f"RP9-{parts[0]}-{parts[1]}-{parts[2]}-{parts[3]}"

def send_license_email(to_email: str, license_key: str):
    url = "https://api.resend.com/emails"
    headers = {
        "Authorization": f"Bearer {RESEND_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "from": f"RP Stealth Security <{MAIL_FROM}>",
        "to": [to_email],
        "subject": "【RP】ご購入ありがとうございます：ライセンスキーのご案内",
        "html": f"""
        <div style="font-family: sans-serif; line-height: 1.6; color: #333; max-width: 600px; margin: auto; padding: 20px; border: 1px solid #eee; border-radius: 8px;">
            <h2 style="color: #1a1a1a; border-bottom: 2px solid #2563eb; padding-bottom: 8px;">ご購入ありがとうございます</h2>
            <p><strong>RP Stealth Security</strong> のライセンス発行が完了いたしました。</p>
            <p>以下のライセンスキーを設定ファイル等に適用してご利用ください。</p>
            <div style="background: #f1f5f9; padding: 16px; border-radius: 6px; font-family: monospace; font-size: 16px; font-weight: bold; color: #0f172a; text-align: center; letter-spacing: 1px; margin: 20px 0;">
                {license_key}
            </div>
            <p style="font-size: 14px; color: #64748b;">
                ※ 本メールは送信専用アドレスより自動配信されています。<br>
                ※ ライセンスキーはお手元に大切に保管してください。
            </p>
            <hr style="border: none; border-top: 1px solid #e2e8f0; margin: 24px 0;">
            <p style="font-size: 12px; color: #94a3b8; text-align: center;">
                合同会社RP / RP Stealth Security Support<br>
                https://github.com/mylife0513-creator/rp-stealth-security
            </p>
        </div>
        """
    }
    res = requests.post(url, json=payload, headers=headers, timeout=10)
    res.raise_for_status()

@app.post("/webhook")
async def stripe_webhook(request: Request, stripe_signature: str = Header(None, alias="stripe-signature")):
    payload = await request.body()
    try:
        event = stripe.Webhook.construct_event(
            payload=payload,
            sig_header=stripe_signature,
            secret=STRIPE_WEBHOOK_SECRET
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Webhook signature verification failed: {e}")

    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        customer_email = session.get("customer_details", {}).get("email") or session.get("customer_email")
        if customer_email:
            license_key = generate_secure_license_key(customer_email)
            try:
                send_license_email(customer_email, license_key)
            except Exception as e:
                return JSONResponse(status_code=500, content={"error": f"Email sending failed: {e}"})

    return {"status": "success"}

@app.get("/health")
def health():
    return {"status": "healthy"}
