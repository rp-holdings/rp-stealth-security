# 🥷 RP Stealth Security
## 不正アクセス者が勝手に自滅する、最強の新発想セキュリティ。
### 従来の防戦一方の消耗戦を終わらせる、世界初・Webシステム向け「ステルストラップ（Active Deception）」迎撃シールド

[![License: Commercial](https://img.shields.io/badge/license-Commercial-blue.svg)](https://buy.stripe.com/eVq4gz8ND2Nx9Vscr1f3a00)
[![Deployment: Docker / Reverse Proxy](https://img.shields.io/badge/deploy-Docker%20%2F%20Proxy-blue.svg)]()
[![Overhead: <0.2ms](https://img.shields.io/badge/latency%20overhead-%3C0.2ms-orange.svg)]()
[![Target: All Web Systems](https://img.shields.io/badge/target-WordPress%20%2F%20Web%20Apps-brightgreen.svg)]()

---

> 🌐 **Looking for the English documentation?**  
> **[👉 Click here to jump to English Version](#-rp-stealth-security-english-version)**

---

> ### **「これまでのセキュリティとは、発想そのものが180度違います。」**
> 
> 高額なWAFを入れても情報漏洩が止まらないのは、**「侵入者を弾く（403 Forbidden）」というやり方自体が攻撃者を育てていたから**です。
> 
> RP Stealth Security は攻撃者を一切ブロックしません。  
> 巧妙な罠に誘い込み、無意味な偽データを掴ませて手ぶらで帰らせ、時間・計算資源・裏社会での信用のすべてを奪って**「割に合わない」と自滅させる**ステルストラップ迎撃システムです。

👉 **[専門知識がない方向けの「超簡単導入マニュアル（NON-TECH-GUIDE）」はこちら](./NON-TECH-GUIDE.md)**

---

## 🚨 「門を閉ざして耐える」時代の限界

* **【守る側】** 365日24時間、何万箇所もある通信経路で1つのミスも許されない（失敗コスト：数千万円〜数億円）
* **【攻撃側】** 自動化ボットやAIを放置し、ノーリスクで1つの穴を見つけるだけ（失敗コスト：ゼロ）

### ❌ 従来のセキュリティ（WAF等）
「403 Forbidden（拒絶）」を返すことで、攻撃者に「別の攻撃手口を試せ」とヒントを与えてしまいます。

### ⭕ RP Stealth Security
「200 OK（成功）」と錯覚させ、精巧なダミーデータを掴ませて満足して立ち去らせます。守る側はノーダメージ、攻撃者だけが時間と大金を浪費して裏社会で信用を失います。

---

## ⚖️ ステルストラップ迎撃の流れ

1. **攻撃者による探索**（SQLi・パス走査・APIキー探索等）
2. **ステルストラップ発動**
   * ① 拒絶せず「200 OK」を即答
   * ② 暗号論的に偽装された無意味な「Ghost Data」を掴ませる
   * ③ 相手のソケット通信だけを低速化（Tarpit）して足止め
3. **正規ユーザー・守る側**
   * 処理負荷 0.2ms 以下。通常業務・サービスを継続
4. **攻撃者の自滅**
   * 入手データが裏取引市場でゴミと発覚し、信用失墜・撤退

---

## 🥋 3つのステルストラップ機構

* **Ghost Payload Injection（偽装注入）**: 攻撃を検知すると正常応答とともに無意味なダミーデータを返却。攻略完了と誤認させて撤退させます。
* **Reverse Tarpit（泥沼足止め）**: スキャンボットへの応答だけを超低速化し、相手の並列スレッドとインフラ費用を強制浪費させます。
* **Zero Signature（完全ステルス）**: 独自ヘッダーやエラー画面を一切出さず、製品の導入有無すら悟らせません。

---

## 💰 費用と効果の比較

| 比較項目 | 従来型 WAF | **RP Stealth Security** |
|:---|:---:|:---:|
| **迎撃思想** | 403 で拒絶（ヒントを与える） | **ステルストラップ（自滅させる）** |
| **攻撃抑止力** | 低（再試行される） | **極大（裏社会での信用失墜）** |
| **導入コスト** | 初期 数百万円〜 / 月額 50万円〜 | **月額 ¥49,800（固定）** |
| **導入工数** | 数週間〜数ヶ月 | **最短 3 分（コンテナを置くだけ）** |
| **誤検知リスク** | 正常通信遮断のリスクあり | **フェイルオープン（正規通信無傷）** |

---

## 🚀 導入方法（最短3分・全Webシステム対応）

### 1. Docker で起動する場合（WordPress / 各種Webアプリ）
```bash
docker run -d \
  -p 80:80 \
  -p 443:443 \
  -e BACKEND_URL="http://your-site:8080" \
  -e LICENSE_KEY="YOUR_KEY" \
  -e MODE="active_deception" \
  rpllc/rp-stealth-shield:latest
```

### 2. Python / FastAPI に直接組み込む場合
```python
from fastapi import FastAPI
import rp_stealth_security as rp

app = FastAPI()
app.add_middleware(
    rp.StealthSecurityMiddleware,
    license_key="YOUR_KEY",
    mode="active_deception"
)
```

👉 **[月額 ¥49,800 で商用ライセンスを取得する（即時自動発行）](https://buy.stripe.com/eVq4gz8ND2Nx9Vscr1f3a00)**  
*(※Stripe 決済完了後、公式ドメイン `support@rp-sec.com` よりライセンスキーが即座に自動送信されます)*

* 特定商取引法に基づく表記および運営者情報は [LEGAL.md](./LEGAL.md) をご確認ください。

<br>

---
---

# 🌐 RP Stealth Security (English Version)
## Attackers Trap Themselves and Self-Destruct.
### End the Asymmetric War of Attrition. The World's First Stealth Trap (Active Deception) Security Shield for All Web Systems.

[![License: Commercial](https://img.shields.io/badge/license-Commercial-blue.svg)](https://buy.stripe.com/eVq4gz8ND2Nx9Vscr1f3a00)
[![Deployment: Docker / Reverse Proxy](https://img.shields.io/badge/deploy-Docker%20%2F%20Proxy-blue.svg)]()
[![Overhead: <0.2ms](https://img.shields.io/badge/latency%20overhead-%3C0.2ms-orange.svg)]()
[![Target: All Web Systems](https://img.shields.io/badge/target-WordPress%20%2F%20Web%20Apps-brightgreen.svg)]()

> ### **"A complete 180-degree paradigm shift from traditional security."**
> 
> Enterprise giants keep suffering data breaches because **blocking attackers with `403 Forbidden` actually trains them to succeed.**
> 
> RP Stealth Security never blocks attackers.  
> Instead, we lure them into an inescapable stealth trap, hand them worthless dummy data disguised as real records, drain their computing resources, and destroy their credibility in underground markets.

---

## 🚨 The Flaw of Traditional Defense

* **[Defenders]** Must be 100% flawless across thousands of paths 24/7/365. (Failure Cost: Millions of Dollars)
* **[Attackers]** Run automated bots with zero risk until they find one flaw. (Failure Cost: $0)

Traditional WAFs return `403 Forbidden`, signaling to bots to modify their payload and retry. RP Stealth deceives them with `200 OK` and synthetic dummy data—ruining their business model while keeping your servers unharmed.

---

## 🥋 Three Core Deception Mechanisms

* **Ghost Payload Injection**: Responds with `200 OK` and realistic dummy data upon attack detection. Attackers assume success and cease probing.
* **Reverse Tarpit**: Artificially throttles response streams back to aggressive bots, freezing their tools and driving up their infrastructure costs.
* **Zero Signature**: Outputs no vendor headers or unique error pages, preventing attackers from detecting the defense mechanism.

---

## 💰 Cost vs. Value Comparison

| Metric | Enterprise WAF | **RP Stealth Security** |
|:---|:---:|:---:|
| **Defense Strategy** | Passive 403 Blocking | **Stealth Trap (Forces Self-Destruction)** |
| **Deterrence** | Low (Attacker retries) | **Maximum (Underground Reputation Ruined)** |
| **Pricing** | $5,000+/mo | **Flat ¥49,800/mo (~$330 USD)** |
| **Setup Time** | Weeks (Complex routing) | **Under 3 minutes (Docker drop-in)** |

---

## 🚀 Quick Deployment (Under 3 Minutes)

### 1. Docker Reverse Proxy (WordPress, PHP, Node.js, etc.)
```bash
docker run -d \
  -p 80:80 \
  -p 443:443 \
  -e BACKEND_URL="http://your-site:8080" \
  -e LICENSE_KEY="YOUR_KEY" \
  -e MODE="active_deception" \
  rpllc/rp-stealth-shield:latest
```

### 2. Python / FastAPI Middleware
```python
from fastapi import FastAPI
import rp_stealth_security as rp

app = FastAPI()
app.add_middleware(
    rp.StealthSecurityMiddleware,
    license_key="YOUR_KEY",
    mode="active_deception"
)
```

👉 **[Get Your Commercial License (Instant Automated Issuance)](https://buy.stripe.com/eVq4gz8ND2Nx9Vscr1f3a00)**  
*(※Upon Stripe checkout, your license key is immediately dispatched from `support@rp-sec.com`)*

* Commercial usage requires an active subscription. Refer to [LEGAL.md](./LEGAL.md) for legal disclosures.