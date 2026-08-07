from __future__ import annotations

from pydantic import BaseModel, Field


class RawListingDTO(BaseModel):
    """Source-shaped listing payload (pre-normalization)."""

    source: str
    external_id: str
    title: str
    listing_url: str
    seller: str = ""
    condition: str = "unknown"
    price_cents: int = 0
    currency: str = "USD"
    image_url: str = ""
    category: str = "unknown"
    manufacturer: str = ""
    model: str = ""
    provides: list[str] = Field(default_factory=list)
    requires: list[str] = Field(default_factory=list)
    reliability_score: float = 5.0
    summary: str = ""


class ListingView(BaseModel):
    id: int
    component_id: int | None = None
    marketplace: str
    title: str
    listing_url: str
    seller: str
    condition: str
    reliability_score: float
    price_cents: int
    currency: str
    image_url: str = ""
    manufacturer: str | None = None
    model: str | None = None
    category: str | None = None


class ComponentView(BaseModel):
    id: int
    category: str
    manufacturer: str
    model: str


class MarketplaceSyncResult(BaseModel):
    sources: list[str]
    fetched: int
    upserted: int


class GoalView(BaseModel):
    text: str


class MasterSlotView(BaseModel):
    category: str
    component: ComponentView
    listing: ListingView | None = None
    locked_at: str


class MasterBuildView(BaseModel):
    slots: list[MasterSlotView]
    total_cents: int
    currency: str = "USD"


class DraftSlotView(BaseModel):
    category: str
    locked: bool = False
    component: ComponentView
    listing: ListingView | None = None


class DraftBuildView(BaseModel):
    id: str
    title: str
    total_cents: int
    currency: str = "USD"
    slots: list[DraftSlotView]


class HomeProjection(BaseModel):
    goal: GoalView
    master: MasterBuildView
    drafts: list[DraftBuildView]


class ComponentGroupView(BaseModel):
    component: ComponentView
    listings: list[ListingView]


class MarketProjection(BaseModel):
    groups: list[ComponentGroupView]
