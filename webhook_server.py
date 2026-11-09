import os
import json
import secrets
import urllib.request
import urllib.error
from fastapi import FastAPI, Request, HTTPException, Header
import stripe

app = FastAPI(title="RP Stealth Security Server")

# ---------------------------------------------------------------------------
# 1. 環境変数取得
# ---------------------------------------------------------------------------
STRIPE_WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET")
RESEND_API_KEY = os.getenv("RESEND_API_KEY")
MAIL_FROM = os.getenv("MAIL_FROM", "onboarding@resend.dev")

# 重複処理防止用キャッシュ (メモリ保持)
PROCESSED_EVENTS = set()


# ---------------------------------------------------------------------------
# 2. CSPRNG ライセンスキー生成ロジック
# ---------------------------------------------------------------------------
def generate_license_key() -> str:
    """
    暗号論的疑似乱数生成器 (CSPRNG) によるセキュアなキー生成
    フォーマット: RP9-XXXXXXXX-XXXXXXXX-XXXXXXXX-XXXXXXXX
    """
    blocks = [secrets.token_hex(4).upper() for _ in range(4)]
    return f"RP9-{'-'.join(blocks)}"


# ---------------------------------------------------------------------------
# 3. Resend REST API メール直接送信
# ---------------------------------------------------------------------------
def send_license_email(to_email: str, license_key: str):
    """
    Resend API (HTTPS POST) を直接呼び出してライセンスキーを配信
    """
    if not RESEND_API_KEY:
        print(f"[MAIL NOTICE] RESEND_API_KEY is not configured. Mock mail for: {to_email}")
        return

    payload = {
        "from": MAIL_FROM,
        "to": [to_email],
        "subject": "【RP】ご購入ありがとうございます：ライセンスキーのご案内",
        "html": f"""
        <div style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; line-height: 1.6; color: #111; max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #e5e7eb; border-radius: 8px;">
            <h2 style="color: #0f172a; margin-top: 0;">ご購入ありがとうございます</h2>
            <p>RP Stealth Security のライセンス発行が完了いたしました。</p>
            <p>以下のライセンスキーを設定ファイル等に適用してご利用ください。</p>
            
            <div style="background-color: #f8fafc; border: 1px solid #cbd5e1; padding: 16px; border-radius: 6px; font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace; font-size: 16px; font-weight: bold; letter-spacing: 1px; color: #0284c7; text-align: center; margin: 24px 0;">
                {license_key}
            </div>
            
            <p style="font-size: 13px; color: #64748b;">
                ※ 本メールは送信専用アドレスより自動配信されています。<br>
                ※ ライセンスキーはお手元に大切に保管してください。
            </p>
            <hr style="border: none; border-top: 1px solid #e2e8f0; margin: 24px 0;" />
            <p style="font-size: 12px; color: #94a3b8; margin-bottom: 0;">合同会社RP / RP Stealth Security Support</p>
        </div>
        """
    }

    req = urllib.request.Request(
        url="https://api.resend.com/emails",
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {RESEND_API_KEY}",
            "Content-Type": "application/json",
            "User-Agent": "RP-Stealth-Server/1.0"
        },
        method="POST"
    )

    try:
        with urllib.request.urlopen(req, timeout=10) as res:
            res_body = res.read().decode("utf-8")
            print(f"[MAIL SUCCESS] Dispatched via Resend API to {to_email}: {res_body}")
    except urllib.error.HTTPError as e:
        error_detail = e.read().decode("utf-8")
        print(f"[MAIL ERROR] Resend API rejected ({e.code}): {error_detail}")
    except Exception as e:
        print(f"[MAIL ERROR] Network error: {str(e)}")


# ---------------------------------------------------------------------------
# 4. エンドポイント定義
# ---------------------------------------------------------------------------
@app.get("/")
def health_check():
    return {"status": "ok", "service": "rp-stealth-security"}


@app.post("/api/stripe-webhook")
async def stripe_webhook(request: Request, stripe_signature: str = Header(None, alias="stripe-signature")):
    payload = await request.body()

    # 署名検証
    if not STRIPE_WEBHOOK_SECRET:
        raise HTTPException(status_code=500, detail="STRIPE_WEBHOOK_SECRET is not configured")

    try:
        event = stripe.Webhook.construct_event(
            payload=payload,
            sig_header=stripe_signature,
            secret=STRIPE_WEBHOOK_SECRET
        )
    except (ValueError, stripe.error.SignatureVerificationError) as err:
        print(f"[SECURITY ALERT] Webhook Signature Verification Failed: {str(err)}")
        raise HTTPException(status_code=400, detail="Invalid signature")

    event_id = event.get("id")

    # 冪等性ガード（重複受信の抑制）
    if event_id in PROCESSED_EVENTS:
        print(f"[WEBHOOK IDEMPOTENT] Duplicate event {event_id} ignored.")
        return {"status": "success", "message": "Duplicate event ignored"}

    # 決済完了イベントのハンドリング
    if event.get("type") == "checkout.session.completed":
        session = event["data"]["obj" + "ect"]
        
        # 顧客メールアドレスの抽出
        customer_email = session.get("customer_details", {}).get("email") or session.get("customer_email")
        if not customer_email:
            customer_email = "unknown@rp-sec.com"

        # ライセンスキー生成
        license_key = generate_license_key()

        print("==================================================")
        print("[SECURITY AUDIT] License Key Issued Successfully")
        print(f"Customer:    {customer_email}")
        print(f"License Key: {license_key}")
        print("==================================================")

        # Resend による実メール送信
        send_license_email(to_email=customer_email, license_key=license_key)

        PROCESSED_EVENTS.add(event_id)

    return {"status": "success"}
