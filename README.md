# RP Stealth Security

> Next-gen In-Line Stealth Security Middleware for Modern Web Frameworks & APIs (FastAPI, Starlette, ASGI/WSGI).

---

## 💡 Why RP Stealth Security? / 導入対効果 & コスト比較

### 従来のセキュリティ対策との比較
従来の境界防御（WAF）や運用体制と比較して、RP Stealth Securityはインフラコストと運用負荷を大幅に削減しながら、ミドルウェア層での即時無力化を提供します。

| 対策アプローチ | 一般的な企業負担コスト | RP Stealth Security (本製品) |
| :--- | :--- | :--- |
| **商用クラウドWAF**<br>(Cloudflare Enterprise / AWS WAF等) | 月額 15万〜50万円超<br>＋ トラフィック従量課金 | **月額 ¥49,800 (定額)**<br>トラフィック従量課金なし・自社インフラ完結 |
| **セキュリティ専任エンジニア**<br>(常駐・運用監視の外注) | 人件費 月額 80万〜150万円 | **自動迎撃・ステルス運用**<br>人手をかけずミドルウェア層で攻撃者を無力化 |
| **インシデント事後対応**<br>(フォレンジック調査・顧客対応) | 1インシデント 数百万円〜数千万円 | **手前での事前遮断**<br>偽装レスポンスと自動シンクで侵入契機を排除 |

### ライセンス体系
- **個人開発・検証環境 (Community)**: **無料** (GitHub / PyPIより自由にご利用いただけます)
- **商用利用・本番運用 (Commercial)**: **¥49,800 / 月** (税込)
  - 商用本番環境での利用権
  - 暗号化商用ライセンスキーの即時自動発行
  - 優先アップデートおよび専用メールサポート (`ops@rp-sec.com`)

👉 **[商用ライセンスを購入して即時有効化する (Stripe決済)](https://buy.stripe.com/eVq4gz8ND2Nx9Vscr1f3a00)**

---

## 🚀 Quick Start

```bash
pip install rp-stealth-security
from fastapi import FastAPI
from rp_stealth_security import StealthSecurityMiddleware

app = FastAPI()
app.add_middleware(
    StealthSecurityMiddleware,
    license_key="COMMERCIAL_LICENSE_KEY_OR_DEV_TOKEN",
    reflection_sink=True,
    chrono_storage=True
)

@app.get("/")
def read_root():
    return {"status": "protected"}
    
