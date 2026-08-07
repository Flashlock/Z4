"""Shared multi-category fixture catalog used by marketplace sources."""

from __future__ import annotations

from api.domain.dtos import RawListingDTO

PLACEHOLDER = "https://placehold.co/160x120/1E293B/C97A2B?text=Z4"


def _item(
    source: str,
    external_id: str,
    title: str,
    category: str,
    manufacturer: str,
    model: str,
    price_cents: int,
    *,
    condition: str = "new",
    reliability: float = 8.0,
    provides: list[str] | None = None,
    requires: list[str] | None = None,
    seller: str | None = None,
) -> RawListingDTO:
    return RawListingDTO(
        source=source,
        external_id=external_id,
        title=title,
        listing_url=f"https://{source}.example/listing/{external_id}",
        seller=seller or source.replace("fixture_", "").title() + "Seller",
        condition=condition,
        price_cents=price_cents,
        image_url=PLACEHOLDER,
        category=category,
        manufacturer=manufacturer,
        model=model,
        provides=provides or [],
        requires=requires or [],
        reliability_score=reliability,
        summary=f"{title} fixture listing.",
    )


def alpha_batch() -> list[RawListingDTO]:
    s = "fixture_alpha"
    return [
        _item(s, "a-cpu-5600", "AMD Ryzen 5 5600", "cpu", "AMD", "Ryzen 5 5600", 12999, provides=["AM4"], requires=["DDR4"], reliability=8.5),
        _item(s, "a-cpu-7600", "AMD Ryzen 5 7600", "cpu", "AMD", "Ryzen 5 7600", 19999, provides=["AM5"], requires=["DDR5"], reliability=9.0),
        _item(s, "a-mobo-b550", "MSI B550 Tomahawk", "motherboard", "MSI", "B550 Tomahawk", 14999, provides=["AM4", "DDR4"], reliability=9.0),
        _item(s, "a-mobo-b650", "Gigabyte B650 Eagle", "motherboard", "Gigabyte", "B650 Eagle", 17999, provides=["AM5", "DDR5"], reliability=8.5),
        _item(s, "a-ram-32-ddr4", "Corsair Vengeance 32GB DDR4", "memory", "Corsair", "Vengeance 32GB DDR4", 7999, provides=["DDR4"], reliability=8.0),
        _item(s, "a-ram-32-ddr5", "G.Skill Flare 32GB DDR5", "memory", "G.Skill", "Flare 32GB DDR5", 10999, provides=["DDR5"], reliability=8.5),
        _item(s, "a-ssd-1tb", "Samsung 980 1TB", "storage", "Samsung", "980 1TB", 6999, provides=["NVMe"], reliability=9.0),
        _item(s, "a-ssd-2tb", "WD SN850X 2TB", "storage", "WD", "SN850X 2TB", 12999, provides=["NVMe"], reliability=8.5),
        _item(s, "a-gpu-6700xt", "AMD RX 6700 XT", "gpu", "AMD", "RX 6700 XT", 28999, provides=["PCIe_x16"], reliability=8.0),
        _item(s, "a-gpu-4070", "NVIDIA RTX 4070", "gpu", "NVIDIA", "RTX 4070", 54999, provides=["PCIe_x16"], reliability=9.0),
        _item(s, "a-psu-650", "Corsair RM650x", "psu", "Corsair", "RM650x", 10999, provides=["ATX_PSU"], reliability=9.0),
        _item(s, "a-psu-750", "Seasonic Focus 750", "psu", "Seasonic", "Focus 750", 12999, provides=["ATX_PSU"], reliability=9.0),
        _item(s, "a-case-4000d", "Corsair 4000D", "case", "Corsair", "4000D", 9999, reliability=8.5),
        _item(s, "a-case-lancool", "Lian Li Lancool 216", "case", "Lian Li", "Lancool 216", 10999, reliability=8.5),
        _item(s, "a-cooler-peerless", "Thermalright Peerless Assassin", "cooler", "Thermalright", "Peerless Assassin", 3599, reliability=8.0),
        _item(s, "a-cooler-nhd15", "Noctua NH-D15", "cooler", "Noctua", "NH-D15", 10999, reliability=9.5),
    ]


def beta_batch() -> list[RawListingDTO]:
    s = "fixture_beta"
    return [
        _item(s, "b-cpu-5600", "R5 5600 used", "cpu", "AMD", "Ryzen 5 5600", 10950, condition="used", reliability=6.0, provides=["AM4"], requires=["DDR4"]),
        _item(s, "b-cpu-7600", "Ryzen 5 7600 box", "cpu", "AMD", "Ryzen 5 7600", 18900, reliability=7.5, provides=["AM5"], requires=["DDR5"]),
        _item(s, "b-mobo-b550", "B550 TOMAHAWK open box", "motherboard", "MSI", "B550 Tomahawk", 13900, condition="used", reliability=7.0, provides=["AM4", "DDR4"]),
        _item(s, "b-mobo-b650", "B650 Eagle", "motherboard", "Gigabyte", "B650 Eagle", 16950, reliability=7.5, provides=["AM5", "DDR5"]),
        _item(s, "b-ram-32-ddr4", "32GB DDR4 kit", "memory", "Corsair", "Vengeance 32GB DDR4", 7499, reliability=7.0, provides=["DDR4"]),
        _item(s, "b-ram-32-ddr5", "Flare DDR5 32GB", "memory", "G.Skill", "Flare 32GB DDR5", 9999, reliability=7.5, provides=["DDR5"]),
        _item(s, "b-ssd-1tb", "980 1TB", "storage", "Samsung", "980 1TB", 6499, reliability=8.0, provides=["NVMe"]),
        _item(s, "b-gpu-6700", "6700XT mining pull", "gpu", "AMD", "RX 6700 XT", 24999, condition="used", reliability=5.5, provides=["PCIe_x16"]),
        _item(s, "b-gpu-4070", "RTX 4070 FE", "gpu", "NVIDIA", "RTX 4070", 52999, reliability=8.5, provides=["PCIe_x16"]),
        _item(s, "b-psu-650", "RM650x", "psu", "Corsair", "RM650x", 9999, reliability=8.0, provides=["ATX_PSU"]),
        _item(s, "b-case-4000d", "4000D Airflow", "case", "Corsair", "4000D", 8999, reliability=8.0),
        _item(s, "b-cooler-pa", "Peerless Assassin 120", "cooler", "Thermalright", "Peerless Assassin", 3299, reliability=7.5),
    ]
