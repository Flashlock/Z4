from __future__ import annotations

from api.db.models import ListingRow, MasterSlotRow
from api.domain.categories import CATEGORIES
from api.domain.dtos import GoalView
from api.ports.build_recommender import RecommendedDraft, RecommendedSlot


class FixtureRecommender:
    """Deterministic mock recommender: 5 full builds (all categories), independent of master locks."""

    def recommend(
        self,
        goal: GoalView,
        master_slots: list[MasterSlotRow],
        listings_by_category: dict[str, list[ListingRow]],
    ) -> list[RecommendedDraft]:
        _ = goal
        _ = master_slots  # drafts stay independent; locking does not rewrite other drafts
        drafts: list[RecommendedDraft] = []
        for index in range(5):
            slots: list[RecommendedSlot] = []
            for category in CATEGORIES:
                options = listings_by_category.get(category) or []
                if not options:
                    continue
                pick = options[index % len(options)]
                slots.append(RecommendedSlot(category=category, listing=pick))
            drafts.append(RecommendedDraft(draft_id=f"draft-{index + 1}", slots=slots))
        return drafts
