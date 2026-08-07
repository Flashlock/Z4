from __future__ import annotations

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from api.db.session import get_session
from api.domain.dtos import GoalView, HomeProjection
from api.repositories.build import BuildRepository
from api.repositories.catalog import CatalogRepository
from api.services.build import BuildService

router = APIRouter(tags=["home"])


class GoalUpdate(BaseModel):
    text: str


def _service(session: Session) -> BuildService:
    return BuildService(CatalogRepository(session), BuildRepository(session))


@router.get("/api/v1/home", response_model=HomeProjection)
def get_home(session: Session = Depends(get_session)) -> HomeProjection:
    return _service(session).get_home()


@router.put("/api/v1/goal", response_model=GoalView)
def put_goal(body: GoalUpdate, session: Session = Depends(get_session)) -> GoalView:
    return _service(session).set_goal(body.text)
