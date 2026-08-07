from __future__ import annotations

from typing import Protocol

from api.domain.dtos import RawListingDTO


class MarketplaceSource(Protocol):
    """Port for marketplace ingestion adapters (fixtures now, scrapers later)."""

    @property
    def name(self) -> str: ...

    def fetch_batch(self) -> list[RawListingDTO]: ...
