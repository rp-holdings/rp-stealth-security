import asyncio
import json
import logging
from datetime import datetime, timezone
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
from .license_validator import LicenseValidator
from .recon_barrier import ReconBarrier

logger = logging.getLogger("rp_stealth_security")

class StealthSecurityMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, license_key: str, mode: str = "active_deception"):
        super().__init__(app)
        self.license_key = license_key
        self.mode = mode
        self.is_valid_license = LicenseValidator.validate(license_key)

    async def dispatch(self, request: Request, call_next):
        if not self.is_valid_license:
            return await call_next(request)

        body_bytes = await request.body()
        body_str = body_bytes.decode("utf-8", errors="ignore")
        
        if ReconBarrier.is_suspicious(request.url.path, request.url.query, body_str):
            if self.mode == "active_deception":
                # Reverse Tarpit (slow down attacker)
                await asyncio.sleep(0.5)

                # Silent Forensics Logging (Preserve evidence while attacker is held)
                forensic_evidence = {
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                    "source_ip": request.client.host if request.client else "unknown",
                    "path": request.url.path,
                    "query": request.url.query,
                    "headers": dict(request.headers),
                    "payload_snippet": body_str[:512],
                    "action": "deception_trap_activated"
                }
                logger.warning(f"[RP_FORENSICS_EVIDENCE] {json.dumps(forensic_evidence)}")

                # Ghost Payload Injection
                dummy_payload = {
                    "status": "success",
                    "code": 200,
                    "records": [
                        {"id": 1042, "role": "guest"},
                        {"id": 1043, "role": "restricted"}
                    ],
                    "query_execution_time": "0.012s"
                }
                return Response(
                    content=json.dumps(dummy_payload),
                    media_type="application/json",
                    status_code=200,
                    headers={
                        "Server": "nginx",
                        "Content-Type": "application/json"
                    }
                )
        return await call_next(request)
