import time
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response, JSONResponse
from .license_verifier import verify_license
from .reflection_sink import ReflectionSink
from .chrono_storage import ChronoStorage

class StealthSecurityMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, license_key: str = "", reflection_sink: bool = True, chrono_storage: bool = True):
        super().__init__(app)
        self.license_key = license_key
        self.is_commercial = verify_license(license_key)
        self.sink = ReflectionSink() if reflection_sink else None
        self.chrono = ChronoStorage() if chrono_storage else None

    async def dispatch(self, request: Request, call_next):
        # 1. Attacker scan / probe detection (e.g., automated scanner paths)
        path = request.url.path.lower()
        if any(p in path for p in [".env", "wp-admin", "eval-stdin", "actuator", ".git"]):
            if self.sink:
                # Reflection Sink: Tarpit & decoy reflection
                return await self.sink.absorb_and_reflect(request)
            return Response(status_code=404)

        # 2. Chrono-Paradox / Tamper verification on state-changing methods
        if request.method in ["POST", "PUT", "DELETE", "PATCH"]:
            if self.chrono and not await self.chrono.verify_flow(request):
                return JSONResponse({"status": "error", "message": "Flow anomaly detected"}, status_code=400)

        response = await call_next(request)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        return response
