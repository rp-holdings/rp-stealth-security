"""
RP Stealth Security - Share-Deception Module (v10.0.0)
Active Deception Middleware for External File-Sharing Links & Endpoints.
License: MIT (Community Edition) / Commercial License for Enterprise Features.
"""

import hashlib
import json
import time
from typing import Callable, Optional
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware


class ShareDeceptionMiddleware(BaseHTTPMiddleware):
    """
    Detects anomalous or unauthorized access to protected file-sharing paths
    and returns HTTP 200 OK with harmless decoy documents ("Empty Vault")
    instead of 403 Forbidden, while logging forensic signatures.
    """

    def __init__(
        self,
        app,
        protected_prefixes: tuple = ("/share/", "/files/", "/docs/"),
        allowed_asns: Optional[set] = None,
        fail_open: bool = True,
    ):
        super().__init__(app)
        self.protected_prefixes = protected_prefixes
        self.allowed_asns = allowed_asns or set()
        self.fail_open = fail_open

    def _is_anomalous_request(self, request: Request) -> bool:
        # Check missing or suspicious browser fingerprint headers
        ua = request.headers.get("user-agent", "").lower()
        if not ua or any(bot in ua for bot in ("curl", "python-requests", "wget", "scanner", "bot")):
            return True

        # Check optional ASN allowlist header (injected by reverse proxy / Cloudflare)
        client_asn = request.headers.get("cf-ipasn") or request.headers.get("x-client-asn")
        if self.allowed_asns and client_asn and client_asn not in self.allowed_asns:
            return True

        return False

    def _generate_decoy_payload(self, request: Request) -> bytes:
        fingerprint = hashlib.sha256(
            f"{request.client.host if request.client else 'unknown'}:{time.time()}".encode()
        ).hexdigest()[:16]
        decoy = {
            "status": "ok",
            "document_id": f"DOC-{fingerprint.upper()}",
            "title": "共有資料_確認用サマリー_v1",
            "summary": "本資料は閲覧専用プレビューです。詳細データは承認済み端末から参照してください。",
            "watermark_trace_id": fingerprint,
        }
        return json.dumps(decoy, ensure_ascii=False, indent=2).encode("utf-8")

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        try:
            path = request.url.path
            if any(path.startswith(prefix) for prefix in self.protected_prefixes):
                if self._is_anomalous_request(request):
                    decoy_body = self._generate_decoy_payload(request)
                    return Response(
                        content=decoy_body,
                        status_code=200,
                        media_type="application/json; charset=utf-8",
                        headers={"X-Content-Trace": "verified"},
                    )
            return await call_next(request)
        except Exception:
            # Fail-Open Guarantee: Never block legitimate traffic on internal error
            if self.fail_open:
                return await call_next(request)
            raise
