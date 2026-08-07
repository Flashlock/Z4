from __future__ import annotations

from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, Float, ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class ComponentRow(Base):
    __tablename__ = "components"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    category: Mapped[str] = mapped_column(String(64), nullable=False)
    manufacturer: Mapped[str] = mapped_column(String(128), nullable=False)
    model: Mapped[str] = mapped_column(String(256), nullable=False)
    specifications_json: Mapped[str] = mapped_column(Text, default="{}")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    __table_args__ = (UniqueConstraint("manufacturer", "model", name="uq_component_identity"),)

    listings: Mapped[list[ListingRow]] = relationship(back_populates="component")


class InterfaceRow(Base):
    __tablename__ = "interfaces"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(128), unique=True, nullable=False)
    description: Mapped[str] = mapped_column(Text, default="")


class ComponentInterfaceRow(Base):
    __tablename__ = "component_interfaces"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    component_id: Mapped[int] = mapped_column(ForeignKey("components.id"), nullable=False)
    interface_id: Mapped[int] = mapped_column(ForeignKey("interfaces.id"), nullable=False)
    direction: Mapped[str] = mapped_column(String(16), nullable=False)  # Provides | Requires

    __table_args__ = (
        UniqueConstraint("component_id", "interface_id", "direction", name="uq_component_interface"),
    )


class ListingRow(Base):
    __tablename__ = "listings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    component_id: Mapped[Optional[int]] = mapped_column(ForeignKey("components.id"), nullable=True)
    marketplace: Mapped[str] = mapped_column(String(64), nullable=False)
    listing_url: Mapped[str] = mapped_column(String(1024), nullable=False)
    seller: Mapped[str] = mapped_column(String(256), default="")
    condition: Mapped[str] = mapped_column(String(64), default="unknown")
    reliability_score: Mapped[float] = mapped_column(Float, default=5.0)
    ai_summary: Mapped[str] = mapped_column(Text, default="")
    title: Mapped[str] = mapped_column(String(512), default="")
    price_cents: Mapped[int] = mapped_column(Integer, default=0)
    currency: Mapped[str] = mapped_column(String(8), default="USD")
    image_url: Mapped[str] = mapped_column(String(1024), default="")
    external_id: Mapped[str] = mapped_column(String(256), default="")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    __table_args__ = (
        UniqueConstraint("marketplace", "external_id", name="uq_listing_marketplace_external"),
    )

    component: Mapped[Optional[ComponentRow]] = relationship(back_populates="listings")


class GoalRow(Base):
    __tablename__ = "goals"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    text: Mapped[str] = mapped_column(Text, default="")
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class MasterSlotRow(Base):
    __tablename__ = "master_slots"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    category: Mapped[str] = mapped_column(String(64), unique=True, nullable=False)
    component_id: Mapped[int] = mapped_column(ForeignKey("components.id"), nullable=False)
    listing_id: Mapped[Optional[int]] = mapped_column(ForeignKey("listings.id"), nullable=True)
    locked_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    component: Mapped[ComponentRow] = relationship()
    listing: Mapped[Optional[ListingRow]] = relationship()
