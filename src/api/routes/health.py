from __future__ import annotations

from fastapi import APIRouter

from api.config import get_settings

router = APIRouter(tags=["health"])


@router.get("/api/v1/health")
def health() -> dict[str, str]:
    settings = get_settings()
    return {
        "instanceId": settings.pantheon_instance_id,
        "agentId": settings.agent_id,
        "status": "ok",
        "version": settings.package_version,
    }
