from __future__ import annotations

from sqlalchemy import inspect, text
from sqlalchemy.engine import Engine

from api.db.models import Base


def ensure_schema(engine: Engine) -> None:
    """Create missing tables and apply lightweight SQLite column upgrades."""
    Base.metadata.create_all(bind=engine)
    _ensure_listings_image_url(engine)


def _ensure_listings_image_url(engine: Engine) -> None:
    inspector = inspect(engine)
    if "listings" not in inspector.get_table_names():
        return
    columns = {col["name"] for col in inspector.get_columns("listings")}
    if "image_url" in columns:
        return
    with engine.begin() as conn:
        conn.execute(
            text("ALTER TABLE listings ADD COLUMN image_url VARCHAR(1024) DEFAULT ''")
        )
