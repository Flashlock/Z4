from __future__ import annotations

import json

from sqlalchemy import func, select
from sqlalchemy.orm import Session, joinedload

from api.db.models import ComponentInterfaceRow, ComponentRow, InterfaceRow, ListingRow
from api.domain.dtos import ComponentGroupView, ComponentView, ListingView, MarketProjection, RawListingDTO


def listing_to_view(row: ListingRow) -> ListingView:
    component = row.component
    return ListingView(
        id=row.id,
        component_id=row.component_id,
        marketplace=row.marketplace,
        title=row.title,
        listing_url=row.listing_url,
        seller=row.seller,
        condition=row.condition,
        reliability_score=row.reliability_score,
        price_cents=row.price_cents,
        currency=row.currency,
        image_url=row.image_url or "",
        manufacturer=component.manufacturer if component else None,
        model=component.model if component else None,
        category=component.category if component else None,
    )


def component_to_view(row: ComponentRow) -> ComponentView:
    return ComponentView(
        id=row.id,
        category=row.category,
        manufacturer=row.manufacturer,
        model=row.model,
    )


class CatalogRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def listing_count(self) -> int:
        return int(self._session.scalar(select(func.count()).select_from(ListingRow)) or 0)

    def upsert_from_raw(self, raw: RawListingDTO) -> ListingRow:
        component = self._get_or_create_component(raw)
        self._sync_interfaces(component, raw)

        listing = self._session.scalar(
            select(ListingRow).where(
                ListingRow.marketplace == raw.source,
                ListingRow.external_id == raw.external_id,
            )
        )
        if listing is None:
            listing = ListingRow(
                marketplace=raw.source,
                external_id=raw.external_id,
            )
            self._session.add(listing)

        listing.component_id = component.id
        listing.listing_url = raw.listing_url
        listing.seller = raw.seller
        listing.condition = raw.condition
        listing.reliability_score = raw.reliability_score
        listing.ai_summary = raw.summary
        listing.title = raw.title
        listing.price_cents = raw.price_cents
        listing.currency = raw.currency
        listing.image_url = raw.image_url
        self._session.flush()
        return listing

    def list_listings(self) -> list[ListingView]:
        rows = self._session.scalars(
            select(ListingRow)
            .options(joinedload(ListingRow.component))
            .order_by(ListingRow.marketplace, ListingRow.id)
        ).unique().all()
        return [listing_to_view(row) for row in rows]

    def get_listing(self, listing_id: int) -> ListingRow | None:
        return self._session.scalar(
            select(ListingRow)
            .options(joinedload(ListingRow.component))
            .where(ListingRow.id == listing_id)
        )

    def get_component(self, component_id: int) -> ComponentRow | None:
        return self._session.get(ComponentRow, component_id)

    def interfaces_for(self, component_id: int) -> tuple[set[str], set[str]]:
        stmt = (
            select(ComponentInterfaceRow.direction, InterfaceRow.name)
            .join(InterfaceRow, ComponentInterfaceRow.interface_id == InterfaceRow.id)
            .where(ComponentInterfaceRow.component_id == component_id)
        )
        provides: set[str] = set()
        requires: set[str] = set()
        for direction, name in self._session.execute(stmt).all():
            if direction == "Provides":
                provides.add(name)
            elif direction == "Requires":
                requires.add(name)
        return provides, requires

    def best_listing_for_component(self, component_id: int) -> ListingRow | None:
        return self._session.scalar(
            select(ListingRow)
            .options(joinedload(ListingRow.component))
            .where(ListingRow.component_id == component_id)
            .order_by(ListingRow.reliability_score.desc(), ListingRow.price_cents.asc())
            .limit(1)
        )

    def listings_by_category(self) -> dict[str, list[ListingRow]]:
        rows = self._session.scalars(
            select(ListingRow).options(joinedload(ListingRow.component))
        ).unique().all()
        by_cat: dict[str, list[ListingRow]] = {}
        for row in rows:
            if not row.component:
                continue
            by_cat.setdefault(row.component.category, []).append(row)
        for listings in by_cat.values():
            listings.sort(key=lambda r: (-r.reliability_score, r.price_cents))
        return by_cat

    def market(self, query: str = "") -> MarketProjection:
        q = query.strip().lower()
        stmt = select(ComponentRow).options(joinedload(ComponentRow.listings)).order_by(
            ComponentRow.category, ComponentRow.manufacturer, ComponentRow.model
        )
        components = self._session.scalars(stmt).unique().all()
        groups: list[ComponentGroupView] = []
        for component in components:
            hay = f"{component.manufacturer} {component.model} {component.category}".lower()
            if q and q not in hay:
                listing_hit = any(
                    q in (lst.title + lst.seller + lst.marketplace).lower() for lst in component.listings
                )
                if not listing_hit:
                    continue
            groups.append(
                ComponentGroupView(
                    component=component_to_view(component),
                    listings=[listing_to_view(lst) for lst in component.listings],
                )
            )
        return MarketProjection(groups=groups)

    def _get_or_create_component(self, raw: RawListingDTO) -> ComponentRow:
        manufacturer = raw.manufacturer.strip() or "Unknown"
        model = raw.model.strip() or raw.title.strip() or raw.external_id
        component = self._session.scalar(
            select(ComponentRow).where(
                ComponentRow.manufacturer == manufacturer,
                ComponentRow.model == model,
            )
        )
        if component is None:
            component = ComponentRow(
                category=raw.category,
                manufacturer=manufacturer,
                model=model,
                specifications_json=json.dumps({}),
            )
            self._session.add(component)
            self._session.flush()
        return component

    def _sync_interfaces(self, component: ComponentRow, raw: RawListingDTO) -> None:
        for name in raw.provides:
            self._link_interface(component.id, name, "Provides")
        for name in raw.requires:
            self._link_interface(component.id, name, "Requires")

    def _link_interface(self, component_id: int, name: str, direction: str) -> None:
        cleaned = name.strip()
        if not cleaned:
            return
        interface = self._session.scalar(select(InterfaceRow).where(InterfaceRow.name == cleaned))
        if interface is None:
            interface = InterfaceRow(name=cleaned, description="")
            self._session.add(interface)
            self._session.flush()

        existing = self._session.scalar(
            select(ComponentInterfaceRow).where(
                ComponentInterfaceRow.component_id == component_id,
                ComponentInterfaceRow.interface_id == interface.id,
                ComponentInterfaceRow.direction == direction,
            )
        )
        if existing is None:
            self._session.add(
                ComponentInterfaceRow(
                    component_id=component_id,
                    interface_id=interface.id,
                    direction=direction,
                )
            )
