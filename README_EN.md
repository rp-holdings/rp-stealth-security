# 🌐 RP Stealth Security (English Documentation)
> 📖 **Deep Dive Technical Architecture Article**:  
> [Defeat Hackers by Faking "200 OK": The Architecture of Active Deception](https://zenn.dev/rp_holdings/articles/20ee5b526ed619/en)
## Attackers Trap Themselves and Self-Destruct.
### End the Asymmetric War of Attrition. The World's First Stealth Trap (Active Deception) Security Shield for All Web Systems.

[![License: Commercial](https://img.shields.io/badge/license-Commercial-blue.svg)](https://buy.stripe.com/eVq4gz8ND2Nx9Vscr1f3a00)
[![Deployment: Docker / Reverse Proxy](https://img.shields.io/badge/deploy-Docker%20%2F%20Proxy-blue.svg)]()
[![Overhead: <0.2ms](https://img.shields.io/badge/latency%20overhead-%3C0.2ms-orange.svg)]()
[![Target: All Web Systems](https://img.shields.io/badge/target-WordPress%20%2F%20Web%20Apps-brightgreen.svg)]()

---

> 🇯🇵 **日本語のドキュメントをお探しですか？**  
> **[👉 日本語版マニュアル（README.md）はこちら](./README.md)**

---

> ### **"A complete 180-degree paradigm shift from traditional security."**
> 
> Enterprise giants keep suffering catastrophic data breaches because **blocking attackers with `403 Forbidden` actually trains them to succeed.**
> 
> RP Stealth Security never blocks attackers.  
> Instead, we lure them into an inescapable stealth trap, hand them worthless dummy data disguised as real records, drain their computing resources, capture digital forensic telemetry, and destroy their credibility in underground markets.

👉 **[Quick Setup Guide for Non-Engineers (NON-TECH-GUIDE)](./NON-TECH-GUIDE.md)**

---

## 🚨 The Flaw of Traditional Defense

* **[Defenders]** Must be 100% flawless across thousands of paths 24/7/365. (Failure Cost: Millions of Dollars)
* **[Attackers]** Run automated bots with zero risk until they find one flaw. (Failure Cost: $0)

Traditional WAFs return `403 Forbidden`, signaling to bots to modify their payload and retry. RP Stealth deceives them with `200 OK` and synthetic dummy data—ruining their business model while keeping your servers unharmed.

---

## 🛡️ Why Is It Completely Safe for Your Infrastructure?

1. **Strict Fail-Open Philosophy**
   * In the rare event of internal exceptions, parsing anomalies, memory pressure, or license errors, RP Stealth Security never drops or blocks incoming business traffic (never produces 500 or 403). It automatically fails open, ensuring 100% service continuity.
2. **Zero False-Positive Outages**
   * Unlike traditional firewalls that sever suspicious customer traffic, deception mechanics inject harmless synthetic payloads only to confirmed malicious probes. Normal customers will never be locked out.
3. **Stateless & Zero Data Retention**
   * RP operates completely statelessly in-memory (<0.2ms overhead). It does not capture, store, or transmit your production databases or private user records.
4. **Zero Interference with Existing Stacks**
   * Operates as an independent reverse proxy container or clean lightweight middleware, requiring zero refactoring of your underlying code.

---

## 🌐 The Network Effect: Psychological Deterrence Multiplies with Adoption

RP Stealth Security is engineered with a **game-theoretic economic deterrent**:

* **Attacker Paranoia**: Malicious actors cannot verify whether extracted records are legitimate credentials or worthless synthetic artifacts.
* **Reputational Destruction in Underground Markets**: Monetizing or leaking fake databases destroys attacker credibility in dark web forums, triggering immediate blacklisting.
* **Negative ROI for Hackers**: As deployment expands globally, attackers burn cloud computing budgets and time only to harvest noise, rendering widespread automated campaigns economically unviable.

---

## ⚖️ Defense & Forensics Workflow

1. **Reconnaissance Probes** (SQLi, directory traversal, API key scraping)
2. **Stealth Trap & Evidence Capture**
   * ① Return instant `200 OK`
   * ② Deliver cryptographically realistic dummy records (Ghost Data)
   * ③ Throttle attacker sockets via reverse tarpit
   * ④ **[Silent Forensics Logging]** Silently capture client IP, headers, behavioral fingerprints, and raw payloads while the socket is delayed
3. **Legitimate Traffic**
   * Sub-0.2ms latency overhead. Seamless operation
4. **Attacker Neutralization & Legal Escalation**
   * Stolen dummy data is rejected on black markets; captured forensics provide undeniable evidence for law enforcement

---

## 🥋 Four Core Defense Mechanisms

* **Ghost Payload Injection**: Responds with `200 OK` and realistic dummy data upon attack detection. Attackers assume success and cease probing.
* **Reverse Tarpit**: Artificially throttles response streams back to aggressive bots, freezing their tools and driving up their infrastructure costs.
* **Silent Forensics Logging**: Captures deep forensic telemetry (source IP, headers, behavioral fingerprints, full exploit payloads) while the attacker is locked in the tarpit, securing decisive evidence for law enforcement and legal retaliation.
* **Zero Signature**: Outputs no vendor headers or unique error pages, preventing attackers from detecting the defense mechanism.

---

## 💰 Cost vs. Value Comparison

| Metric | Enterprise WAF | **RP Stealth Security** |
|:---|:---:|:---:|
| **Defense Strategy** | Passive 403 Blocking | **Stealth Trap (Forces Self-Destruction)** |
| **Deterrence** | Low (Attacker retries) | **Maximum (Underground Reputation Ruined)** |
| **Evidence Gathering** | Basic blocked IP log | **Full telemetry & payload capture during tarpit** |
| **Pricing** | $5,000+/mo | **Flat ¥49,800/mo (~$330 USD)** |
| **Setup Time** | Weeks (Complex routing) | **Under 3 minutes (Docker drop-in)** |
| **False-Positive Risk** | High (Blocks real buyers) | **Fail-Open (Harmless to real users)** |

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
