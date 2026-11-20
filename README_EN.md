# RP Stealth Security (v10.0.0)

**Active Deception Reverse Proxy & Middleware for Web Systems**

Instead of blocking unauthorized access with standard error codes such as `403 Forbidden`—which alerts attackers and automated scanning AI to the presence of defensive controls—**RP Stealth Security** responds with `200 OK` and harmless decoy payloads. This isolates malicious probes in a controlled deception layer while keeping legitimate business traffic unaffected.

---

## 1. Key Capabilities & Architecture

Traditional perimeter defenses (WAFs and IP blocklists) inadvertently provide reconnaissance feedback whenever they drop or reject requests. RP Stealth Security evaluates request context and behavioral anomalies across multiple layers, silently routing suspicious traffic to a decoy response handler.

* **Stealth `200 OK` Deception Responses**
  * Returns `200 OK` status codes paired with configurable, harmless decoy data (JSON, HTML, or synthetic document previews) upon detecting automated vulnerability scans or unauthorized probes.
* **External File-Sharing Link Protection (`ShareDeceptionMiddleware` / New in v10.0.0)**
  * Protects shared URLs and document delivery endpoints. When an access request originates from an unrecognized network context, anomalous fingerprint, or enumeration query, the middleware isolates the authentic file and serves a read-only decoy document while logging forensic metadata.
* **Socket Tarpit & Forensic Telemetry**
  * Introduces controlled response latency (Tarpit) to degrade the throughput of automated scanners and records structured forensic logs for incident investigation.
* **Language- & Stack-Agnostic Deployment (Zero Code Changes Required)**
  * Deployed as an independent reverse-proxy Docker container in front of existing web applications (ports 80/443), supporting any backend stack (Java, PHP, Go, Node.js, .NET, or legacy systems) without modifying application source code. Native Python (FastAPI/ASGI) middleware integration is also supported.

---

## 2. Quick Start (Docker Reverse Proxy)

Launch the deception proxy in front of an existing backend service (e.g., `127.0.0.1:8080`):

```bash
docker run -d \
  --name rp-stealth-shield \
  --restart always \
  -p 80:80 -p 443:443 \
  -e BACKEND_URL="http://127.0.0.1:8080" \
  -e LICENSE_KEY="RP9-YOUR-PURCHASED-KEY" \
  rp-holdings/rp-stealth-security:10.0.0
```

### Native Python (FastAPI) Middleware Integration

```python
from fastapi import FastAPI
from rp_stealth_security import StealthMiddleware, ShareDeceptionMiddleware

app = FastAPI()

# Core Active Deception Middleware
app.add_middleware(StealthMiddleware)

# Deception Protection for Shared Links & Document Endpoints (v10.0.0)
app.add_middleware(
    ShareDeceptionMiddleware,
    protected_prefixes=["/share/", "/docs/"],
    whitelist_ips=["10.0.0.0/8", "192.168.0.0/16"],
)
```

---

## 3. Four Core Design Principles for Availability & Compliance

Enterprise and public-sector deployments require strict guarantees against service disruption and regulatory violations. RP Stealth Security is engineered around four foundational principles:

1. **Fail-Open Architecture**
   * In the event of internal exceptions, parsing errors, memory pressure, or license validation failures, the middleware immediately bypasses inspection and forwards legitimate HTTP requests directly to the upstream backend rather than returning `500` or `403` errors.
2. **Mitigation of False-Positive Service Outages**
   * Rather than dropping connections outright when anomaly thresholds are triggered, the engine routes flagged requests to a decoy response handler. Even if an edge-case legitimate request triggers a rule, system availability is preserved.
3. **Strict Non-Retaliatory Compliance (No Hack-Back)**
   * The software contains zero offensive, counter-attack, or remote-access capabilities. All deception mechanisms operate strictly within the boundaries of defensive isolation and comply with applicable cybersecurity statutes.
4. **Zero-Disk Payload Persistence & Edge Privacy**
   * Inspected traffic, shared document contents, and user payloads are never transmitted to external telemetry servers or persisted to disk, supporting compliance with GDPR and enterprise data-governance policies.

---

## 4. Administrative Bypass & Whitelisting

To ensure system administrators and authorized penetration testers can perform maintenance and security audits without triggering deception routing, bypass controls are evaluated prior to anomaly inspection:

* **Source IP / CIDR Whitelisting**: Traffic originating from trusted corporate networks, administrative VPNs, or internal subnets is forwarded directly to the backend.
* **Dry-Run (Observation) Mode**: Evaluates detection rules and logs telemetry without serving decoy responses, allowing safe validation prior to enforcement.

---

## 5. Links & License

* **PyPI Package**: [https://pypi.org/project/rp-stealth-security/](https://pypi.org/project/rp-stealth-security/)
* **Technical Architecture Article (Zenn / JA)**: [https://zenn.dev/rp_holdings/articles/20ee5b526ed619](https://zenn.dev/rp_holdings/articles/20ee5b526ed619)
* **Background & Concept (note / JA)**: [https://note.com/rp_holdings/n/n3ec9c7fec39d](https://note.com/rp_holdings/n/n3ec9c7fec39d)
* **License**: MIT License (Provided "AS IS", without warranty of any kind)
* **Contact**: `support@rp-sec.com` (Asynchronous email support)
