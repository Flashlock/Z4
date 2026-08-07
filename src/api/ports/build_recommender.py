from __future__ import annotations

from typing import Protocol

from api.db.models import ListingRow, MasterSlotRow
from api.domain.dtos import GoalView


class RecommendedSlot:
    def __init__(self, category: str, listing: ListingRow) -> None:
        self.category = category
        self.listing = listing


class RecommendedDraft:
    def __init__(self, draft_id: str, slots: list[RecommendedSlot]) -> None:
        self.draft_id = draft_id
        self.slots = slots


class BuildRecommender(Protocol):
    def recommend(
        self,
        goal: GoalView,
        master_slots: list[MasterSlotRow],
        listings_by_category: dict[str, list[ListingRow]],
    ) -> list[RecommendedDraft]: ...
