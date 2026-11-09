# RP Stealth Security V9 (Enterprise Edition)

[![License](https://img.shields.io/badge/License-Proprietary-blue.svg)](LEGAL.md)
[![Python](https://img.shields.io/badge/Python-3.10%20%7C%203.11%20%7C%203.12-brightgreen.svg)]()
[![Stripe Protected](https://img.shields.io/badge/Payments-Stripe%20Automated-635BFF.svg)](LEGAL.md)

[English](#english-overview) | [日本語](#日本語概要)

---

## 日本語概要

RP Stealth Security V9 は、ゼロ露出・動的デコイルーティング技術を搭載した次世代型エンタープライズ・サイバーセキュリティ・スイートです。従来のファイアウォールやWAFのように「検知してブロック（遮断を敵に認知させる）」のではなく、**外部偵察スキャンを完全無力化（ステルス化）し、攻撃者を無害な隔離デコイ層へ自動転送**します。

### 従来型セキュリティ製品との防御比較

| 項目 | 従来のWAF / UTM | RP Stealth Security V9 |
| :--- | :--- | :--- |
| **外部偵察（ポートスキャン等）** | 拒絶（RST/Drop）を返し存在を暴露 | 応答そのものを完全ステルス化（ゼロ露出） |
| **不正アクセスへの対応** | IPブロック（攻撃者に遮断を覚知される） | 動的デコイルーティング（隔離環境へ幽閉） |
| **標的型・執拗な攻撃者** | IP変更・別経路で再試行される | デコイ層内で無駄な試行を消費させ無力化 |
| **ライセンス自動化** | 手動認証・キー管理の遅延 | Stripe Webhook連携による暗号学的即時自動発行 |

### 商用ライセンスの購入

本製品はサブスクリプション方式で提供されています。決済完了後、Stripe Webhook により暗号学的ライセンスキーが即時自動発行され、ご登録メールアドレスへ送付されます。

- **Enterprise Monthly License**: **¥49,800 / 月（税込）**
- **決済リンク**: [RP Stealth Security V9 を購入する（Stripe安全決済）](https://buy.stripe.com/eVq4gz8ND2Nx9Vscr1f3a00)

---

## English Overview

RP Stealth Security V9 is a next-generation enterprise cyber defense suite equipped with Zero-Exposure Reconnaissance Barriers and Dynamic Decoy Routing. Rather than simply blocking and alerting attackers, V9 completely conceals network footprints and silently diverts hostile probes into isolated decoy layers.

### Comparison Matrix

| Feature | Legacy WAF / UTM | RP Stealth Security V9 |
| :--- | :--- | :--- |
| **Reconnaissance Probing** | Drops/Rejects packets (Exposes presence) | Complete stealth silence (Zero exposure) |
| **Intrusion Response** | Static IP bans (Alerts the adversary) | Dynamic Decoy Routing (Transparent quarantine) |
| **Persistent Threats** | Attacker switches IP and retries | Absorbs malicious payloads in harmless sinkholes |
| **License Provisioning** | Manual processing delays | Fully automated cryptographic Stripe webhook |

### Commercial Licensing

Available via enterprise subscription. License keys are cryptographically generated (CSPRNG) and dispatched immediately upon payment confirmation.

- **Enterprise License**: **JPY 49,800 / month**
- **Direct Purchase**: [Subscribe via Stripe Secure Checkout](https://buy.stripe.com/eVq4gz8ND2Nx9Vscr1f3a00)

---

## 体系・機能構成

1. **Reconnaissance Barrier (`rp_stealth_security/recon_barrier.py`)**: 外部偵察スキャン、Botプローブを低遅延で完全遮断・ステルス化
2. **Decoy Router (`rp_stealth_security/decoy_router.py`)**: 不正侵入試行トラフィックをリアルタイムで隔離ハニーポットへルーティング
3. **Cryptographic License Engine (`rp_stealth_security/license_validator.py`)**: CSPRNG暗号学的キー発行・HMAC検証モジュール
4. **Stripe Webhook Gateway (`webhook_server.py`)**: 決済連動ライセンス自動発行・重複遮断・非同期配信

---

## インストールと起動手順

### 1. 依存ライブラリのインストール
```bash
pip install -r requirements.txt
