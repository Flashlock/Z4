from __future__ import annotations

from api.adapters.fixture_catalog import beta_batch
from api.domain.dtos import RawListingDTO


class FixtureBetaSource:
    @property
    def name(self) -> str:
        return "fixture_beta"

    def fetch_batch(self) -> list[RawListingDTO]:
        return beta_batch()
