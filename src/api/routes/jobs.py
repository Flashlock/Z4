from __future__ import annotations

from typing import Literal

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from api.db.session import get_session
from api.domain.dtos import MarketplaceSyncResult
from api.repositories.catalog import CatalogRepository
from api.services.marketplace_sync import MarketplaceSyncService

router = APIRouter(tags=["jobs"])


class MarketplaceSyncRequest(BaseModel):
    mode: Literal["incremental", "full"] = "incremental"


@router.post(
    "/api/v1/jobs/marketplace-sync",
    response_model=MarketplaceSyncResult,
    status_code=202,
)
def marketplace_sync(
    body: MarketplaceSyncRequest | None = None,
    session: Session = Depends(get_session),
) -> MarketplaceSyncResult:
    payload = body or MarketplaceSyncRequest()
    _ = payload.mode  # reserved for later incremental vs full scrape semantics
    service = MarketplaceSyncService(CatalogRepository(session))
    return service.run()
