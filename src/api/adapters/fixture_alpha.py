from __future__ import annotations

from api.adapters.fixture_catalog import alpha_batch
from api.domain.dtos import RawListingDTO


class FixtureAlphaSource:
    @property
    def name(self) -> str:
        return "fixture_alpha"

    def fetch_batch(self) -> list[RawListingDTO]:
        return alpha_batch()
