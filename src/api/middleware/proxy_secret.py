from __future__ import annotations

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse, Response

from api.config import get_settings

PUBLIC_PATHS = {
    "/api/v1/health",
    "/docs",
    "/openapi.json",
    "/redoc",
}


class ProxySecretMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:  # type: ignore[no-untyped-def]
        path = request.url.path
        if path in PUBLIC_PATHS or path.startswith("/docs") or path.startswith("/redoc"):
            return await call_next(request)

        settings = get_settings()
        provided = request.headers.get("x-pantheon-proxy-secret")
        if not provided or provided != settings.pantheon_proxy_secret:
            return JSONResponse(
                status_code=401,
                content={"error": "INVALID_PROXY_SECRET"},
            )
        return await call_next(request)
