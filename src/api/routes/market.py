from __future__ import annotations

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from api.db.session import get_session
from api.domain.dtos import MarketProjection
from api.repositories.build import BuildRepository
from api.repositories.catalog import CatalogRepository
from api.services.build import BuildService

router = APIRouter(tags=["market"])


@router.get("/api/v1/market", response_model=MarketProjection)
def get_market(
    q: str = Query(default=""),
    session: Session = Depends(get_session),
) -> MarketProjection:
    return BuildService(CatalogRepository(session), BuildRepository(session)).market(q)
