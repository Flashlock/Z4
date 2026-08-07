from __future__ import annotations

from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from api.db.models import GoalRow, ListingRow, MasterSlotRow
from api.domain.dtos import GoalView, MasterBuildView, MasterSlotView
from api.repositories.catalog import component_to_view, listing_to_view


class BuildRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def get_goal(self) -> GoalView:
        row = self._session.scalar(select(GoalRow).order_by(GoalRow.id.asc()).limit(1))
        if row is None:
            return GoalView(text="")
        return GoalView(text=row.text)

    def set_goal(self, text: str) -> GoalView:
        row = self._session.scalar(select(GoalRow).order_by(GoalRow.id.asc()).limit(1))
        if row is None:
            row = GoalRow(text=text, updated_at=datetime.utcnow())
            self._session.add(row)
        else:
            row.text = text
            row.updated_at = datetime.utcnow()
        self._session.flush()
        return GoalView(text=row.text)

    def list_master_slots(self) -> list[MasterSlotRow]:
        return list(
            self._session.scalars(
                select(MasterSlotRow)
                .options(
                    joinedload(MasterSlotRow.component),
                    joinedload(MasterSlotRow.listing).joinedload(ListingRow.component),
                )
                .order_by(MasterSlotRow.category)
            )
            .unique()
            .all()
        )

    def get_master_build(self) -> MasterBuildView:
        slots: list[MasterSlotView] = []
        total = 0
        currency = "USD"
        for row in self.list_master_slots():
            listing_view = None
            if row.listing is not None:
                listing_view = listing_to_view(row.listing)
                total += listing_view.price_cents
                currency = listing_view.currency or currency
            slots.append(
                MasterSlotView(
                    category=row.category,
                    component=component_to_view(row.component),
                    listing=listing_view,
                    locked_at=row.locked_at.isoformat() + "Z",
                )
            )
        return MasterBuildView(slots=slots, total_cents=total, currency=currency)

    def locked_categories(self) -> set[str]:
        return {row.category for row in self.list_master_slots()}

    def upsert_slot(self, category: str, component_id: int, listing_id: int | None) -> MasterSlotRow:
        row = self._session.scalar(select(MasterSlotRow).where(MasterSlotRow.category == category))
        if row is None:
            row = MasterSlotRow(category=category)
            self._session.add(row)
        row.component_id = component_id
        row.listing_id = listing_id
        row.locked_at = datetime.utcnow()
        self._session.flush()
        return row

    def delete_slot(self, category: str) -> bool:
        row = self._session.scalar(select(MasterSlotRow).where(MasterSlotRow.category == category))
        if row is None:
            return False
        self._session.delete(row)
        self._session.flush()
        return True
