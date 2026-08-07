from __future__ import annotations

from api.adapters.fixture_alpha import FixtureAlphaSource
from api.adapters.fixture_beta import FixtureBetaSource
from api.ports.marketplace_source import MarketplaceSource


def default_marketplace_sources() -> list[MarketplaceSource]:
    return [FixtureAlphaSource(), FixtureBetaSource()]
