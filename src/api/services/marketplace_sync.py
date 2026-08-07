from __future__ import annotations

from api.adapters.registry import default_marketplace_sources
from api.domain.dtos import MarketplaceSyncResult
from api.ports.marketplace_source import MarketplaceSource
from api.repositories.catalog import CatalogRepository


class MarketplaceSyncService:
    def __init__(
        self,
        repo: CatalogRepository,
        sources: list[MarketplaceSource] | None = None,
    ) -> None:
        self._repo = repo
        self._sources = sources if sources is not None else default_marketplace_sources()

    def run(self) -> MarketplaceSyncResult:
        fetched = 0
        upserted = 0
        source_names: list[str] = []
        for source in self._sources:
            source_names.append(source.name)
            batch = source.fetch_batch()
            fetched += len(batch)
            for raw in batch:
                self._repo.upsert_from_raw(raw)
                upserted += 1
        return MarketplaceSyncResult(sources=source_names, fetched=fetched, upserted=upserted)
