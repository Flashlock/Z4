from __future__ import annotations

import logging
import traceback
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from api.config import load_manifest
from api.db.session import init_db, session_scope
from api.middleware.proxy_secret import ProxySecretMiddleware
from api.repositories.build import BuildRepository
from api.repositories.catalog import CatalogRepository
from api.routes import builds, health, home, jobs, listings, market, shutdown
from api.services.build import BuildService

logger = logging.getLogger("z4")


@asynccontextmanager
async def lifespan(_app: FastAPI):
    init_db()
    with session_scope() as session:
        BuildService(CatalogRepository(session), BuildRepository(session)).ensure_catalog()
    yield


_manifest = load_manifest()
app = FastAPI(
    title=str(_manifest.get("packageName", "Z4")),
    version=str(_manifest["version"]),
    description=str(_manifest.get("description", "")),
    lifespan=lifespan,
)
app.add_middleware(ProxySecretMiddleware)
app.include_router(health.router)
app.include_router(shutdown.router)
app.include_router(jobs.router)
app.include_router(listings.router)
app.include_router(home.router)
app.include_router(builds.router)
app.include_router(market.router)


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(_request: Request, exc: StarletteHTTPException) -> JSONResponse:
    detail = exc.detail
    if isinstance(detail, dict):
        content = {
            "error": str(detail.get("error") or type(exc).__name__),
            "message": str(detail.get("message") or detail),
            "detail": detail,
        }
        if "conflicts" in detail:
            content["conflicts"] = detail["conflicts"]
        return JSONResponse(status_code=exc.status_code, content=content)
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": type(exc).__name__,
            "message": str(detail),
            "detail": detail,
        },
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    _request: Request, exc: RequestValidationError
) -> JSONResponse:
    return JSONResponse(
        status_code=422,
        content={
            "error": "RequestValidationError",
            "message": str(exc),
            "detail": exc.errors(),
        },
    )


@app.exception_handler(Exception)
async def unhandled_exception_handler(_request: Request, exc: Exception) -> JSONResponse:
    tb = traceback.format_exc()
    logger.exception("Unhandled error")
    return JSONResponse(
        status_code=500,
        content={
            "error": type(exc).__name__,
            "message": str(exc) or type(exc).__name__,
            "traceback": tb,
        },
    )


def create_app() -> FastAPI:
    return app
