import asyncio
from starlette.responses import JSONResponse

class ReflectionSink:
    async def absorb_and_reflect(self, request):
        # Introduce a micro-tarpit delay to exhaust attacker reconnaissance scanners
        await asyncio.sleep(0.35)
        # Return plausible synthetic decoy payload
        return JSONResponse(
            {
                "status": "ok",
                "system": "nginx/1.24.0",
                "telemetry": "logged"
            },
            status_code=200
        )
