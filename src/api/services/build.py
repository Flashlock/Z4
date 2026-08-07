from __future__ import annotations

from fastapi import HTTPException

from api.adapters.builds.fixture_recommender import FixtureRecommender
from api.adapters.builds.fixture_title_writer import FixtureTitleWriter
from api.db.models import ComponentRow
from api.domain.compatibility import ComponentInterfaces, evaluate_build, label_for
from api.domain.dtos import (
    DraftBuildView,
    DraftSlotView,
    GoalView,
    HomeProjection,
    MarketProjection,
)
from api.ports.build_recommender import BuildRecommender, RecommendedDraft
from api.ports.build_title_writer import BuildTitleWriter
from api.repositories.build import BuildRepository
from api.repositories.catalog import CatalogRepository, component_to_view, listing_to_view
from api.services.marketplace_sync import MarketplaceSyncService


class BuildService:
    def __init__(
        self,
        catalog: CatalogRepository,
        builds: BuildRepository,
        recommender: BuildRecommender | None = None,
        title_writer: BuildTitleWriter | None = None,
    ) -> None:
        self._catalog = catalog
        self._builds = builds
        self._recommender = recommender or FixtureRecommender()
        self._titles = title_writer or FixtureTitleWriter()

    def ensure_catalog(self) -> None:
        if self._catalog.listing_count() == 0:
            MarketplaceSyncService(self._catalog).run()

    def get_home(self) -> HomeProjection:
        self.ensure_catalog()
        goal = self._builds.get_goal()
        master = self._builds.get_master_build()
        master_rows = self._builds.list_master_slots()
        recommended = self._recommender.recommend(
            goal, master_rows, self._catalog.listings_by_category()
        )
        drafts = [self._to_draft_view(goal, draft) for draft in recommended]
        return HomeProjection(goal=goal, master=master, drafts=drafts)

    def set_goal(self, text: str) -> GoalView:
        return self._builds.set_goal(text.strip())

    def market(self, query: str = "") -> MarketProjection:
        self.ensure_catalog()
        return self._catalog.market(query)

    def lock_component(self, component_id: int, listing_id: int | None) -> HomeProjection:
        component = self._catalog.get_component(component_id)
        if component is None:
            raise HTTPException(status_code=404, detail="COMPONENT_NOT_FOUND")

        if listing_id is not None:
            listing = self._catalog.get_listing(listing_id)
            if listing is None:
                raise HTTPException(status_code=404, detail="LISTING_NOT_FOUND")
            if listing.component_id != component_id:
                raise HTTPException(status_code=400, detail="LISTING_COMPONENT_MISMATCH")

        self._assert_compatible_with_master([component])
        self._builds.upsert_slot(component.category, component_id, listing_id)
        return self.get_home()

    def lock_draft(self, draft_id: str) -> HomeProjection:
        self.ensure_catalog()
        goal = self._builds.get_goal()
        master_rows = self._builds.list_master_slots()
        recommended = self._recommender.recommend(
            goal, master_rows, self._catalog.listings_by_category()
        )
        draft = next((d for d in recommended if d.draft_id == draft_id), None)
        if draft is None:
            raise HTTPException(status_code=404, detail="DRAFT_NOT_FOUND")

        candidates: list[ComponentRow] = []
        locks: list[tuple[str, int, int]] = []
        for slot in draft.slots:
            listing = slot.listing
            if listing.component_id is None or listing.component is None:
                continue
            candidates.append(listing.component)
            locks.append((slot.category, listing.component_id, listing.id))

        self._assert_compatible_with_master(candidates, replace_categories={c for c, _, _ in locks})

        for category, component_id, listing_id in locks:
            self._builds.upsert_slot(category, component_id, listing_id)
        return self.get_home()

    def unlock(self, category: str) -> HomeProjection:
        if not self._builds.delete_slot(category):
            raise HTTPException(status_code=404, detail="SLOT_NOT_FOUND")
        return self.get_home()

    def _assert_compatible_with_master(
        self,
        incoming: list[ComponentRow],
        replace_categories: set[str] | None = None,
    ) -> None:
        if replace_categories is None:
            replace_categories = {c.category for c in incoming}

        proposed: dict[str, ComponentRow] = {}
        for row in self._builds.list_master_slots():
            if row.category in replace_categories:
                continue
            proposed[row.category] = row.component

        for component in incoming:
            proposed[component.category] = component

        interfaces = [self._component_interfaces(c) for c in proposed.values()]
        conflicts = evaluate_build(interfaces)
        if conflicts:
            raise HTTPException(
                status_code=409,
                detail={
                    "error": "INCOMPATIBLE_WITH_MASTER",
                    "message": "Lock blocked - incompatible with master build graph",
                    "conflicts": conflicts,
                },
            )

    def _component_interfaces(self, component: ComponentRow) -> ComponentInterfaces:
        provides, requires = self._catalog.interfaces_for(component.id)
        return ComponentInterfaces(
            component_id=component.id,
            category=component.category,
            label=label_for(component),
            provides=frozenset(provides),
            requires=frozenset(requires),
        )

    def _to_draft_view(self, goal: GoalView, draft: RecommendedDraft) -> DraftBuildView:
        """Drafts always show their own suggestions + lock actions (independent of master)."""
        slots: list[DraftSlotView] = []
        total = 0
        for slot in draft.slots:
            component = slot.listing.component
            if component is None:
                continue
            listing_view = listing_to_view(slot.listing)
            total += listing_view.price_cents
            slots.append(
                DraftSlotView(
                    category=slot.category,
                    locked=False,
                    component=component_to_view(component),
                    listing=listing_view,
                )
            )

        return DraftBuildView(
            id=draft.draft_id,
            title=self._titles.title_for(goal, draft),
            total_cents=total,
            slots=slots,
        )
