from __future__ import annotations

from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel
from sqlalchemy.orm import Session

from api.db.session import get_session
from api.domain.dtos import HomeProjection
from api.repositories.build import BuildRepository
from api.repositories.catalog import CatalogRepository
from api.services.build import BuildService

router = APIRouter(tags=["builds"])


class LockDraftBody(BaseModel):
    draftId: str


class UnlockBody(BaseModel):
    category: str


def _service(session: Session) -> BuildService:
    return BuildService(CatalogRepository(session), BuildRepository(session))


@router.post(
    "/api/v1/builds/lock/component/{component_id}",
    response_model=HomeProjection,
)
def lock_component(
    component_id: int,
    listing: int | None = Query(default=None),
    session: Session = Depends(get_session),
) -> HomeProjection:
    return _service(session).lock_component(component_id, listing)


@router.post("/api/v1/builds/lock/draft", response_model=HomeProjection)
def lock_draft(body: LockDraftBody, session: Session = Depends(get_session)) -> HomeProjection:
    return _service(session).lock_draft(body.draftId)


@router.post("/api/v1/builds/unlock", response_model=HomeProjection)
def unlock(body: UnlockBody, session: Session = Depends(get_session)) -> HomeProjection:
    return _service(session).unlock(body.category)
