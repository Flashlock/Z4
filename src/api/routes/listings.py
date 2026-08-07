from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from api.db.session import get_session
from api.domain.dtos import ListingView
from api.repositories.catalog import CatalogRepository

router = APIRouter(tags=["listings"])


@router.get("/api/v1/listings", response_model=list[ListingView])
def list_listings(session: Session = Depends(get_session)) -> list[ListingView]:
    return CatalogRepository(session).list_listings()
