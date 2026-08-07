from __future__ import annotations

from typing import Protocol

from api.domain.dtos import GoalView
from api.ports.build_recommender import RecommendedDraft


class BuildTitleWriter(Protocol):
    def title_for(self, goal: GoalView, draft: RecommendedDraft) -> str: ...
