# RP Stealth Security V9 (Enterprise Edition)

[![License](https://img.shields.io/badge/License-Proprietary-blue.svg)](LEGAL.md)
[![Python](https://img.shields.io/badge/Python-3.10%20%7C%203.11%20%7C%203.12-brightgreen.svg)]()

RP Stealth Security V9 は、ゼロ露出・動的デコイルーティング技術を搭載した次世代型エンタープライズ・サイバーセキュリティ・スイートです。

---

## 体系・機能構成

1. **Reconnaissance Barrier (`recon_barrier.py`)**: 外部偵察スキャン、Botプローブを完全遮断・ステルス化
2. **Decoy Router (`decoy_router.py`)**: 不正侵入試行トラフィックをリアルタイムで隔離ハニーポットへルーティング
3. **Cryptographic License Engine (`license_validator.py`)**: CSPRNG暗号学的キー発行・改ざん防止・検証モジュール
4. **Stripe Webhook Gateway (`webhook_server.py`)**: 決済連動ライセンス自動発行・重複遮断・非同期配信

---

## インストールと起動

### 1. 依存関係のセットアップ
```bash
pip install -r requirements.txt
```

### 2. 環境変数の設定
`.env.example` を基に環境変数を設定してください。

```cmd
set STRIPE_WEBHOOK_SECRET=whsec_...
```

### 3. Webhookサーバー起動
```bash
python -m uvicorn webhook_server:app --port 8000
```
