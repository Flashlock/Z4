from __future__ import annotations

from dataclasses import dataclass

from api.db.models import ComponentRow


@dataclass(frozen=True)
class ComponentInterfaces:
    component_id: int
    category: str
    label: str
    provides: frozenset[str]
    requires: frozenset[str]


_FAMILIES = (
    "am5",
    "am4",
    "lga1700",
    "lga1200",
    "ddr5",
    "ddr4",
    "atx",
    "pcie",
)


def normalize_interface(name: str) -> str:
    n = " ".join(name.strip().lower().replace("-", " ").replace("_", " ").split())
    for prefix in ("socket ", "dimm "):
        if n.startswith(prefix):
            n = n[len(prefix) :]
    return n.replace(" ", "")


def _satisfied(requirement: str, provides: set[str]) -> bool:
    req = normalize_interface(requirement)
    if req in provides:
        return True
    return any(req in p or p in req for p in provides if p)


def _family(name: str) -> str | None:
    n = normalize_interface(name)
    for fam in _FAMILIES:
        if fam in n:
            return fam
    return None


def _incompatible_pair(requirement: str, provide: str) -> bool:
    """True when provide is in the same interface family as requirement but does not satisfy it."""
    if _satisfied(requirement, {provide}):
        return False
    rf, pf = _family(requirement), _family(provide)
    return rf is not None and rf == pf


def evaluate_build(components: list[ComponentInterfaces]) -> list[str]:
    """
    Return conflict messages for hard incompatibilities.

    Missing providers (incomplete master) are allowed — e.g. locking a motherboard
    before a PSU is fine. Conflicts fire when another locked part provides a
    competing interface in the same family that does not satisfy the requirement
    (AM4 board vs AM5 CPU, DDR4 vs DDR5, etc.).
    """
    if len(components) < 2:
        return []

    conflicts: list[str] = []
    for comp in components:
        for req in sorted(comp.requires):
            for other in components:
                if other.component_id == comp.component_id:
                    continue
                for provide in sorted(other.provides):
                    if _incompatible_pair(req, provide):
                        conflicts.append(
                            f"{comp.label} requires '{req}', but {other.label} provides '{provide}'"
                        )
    # Deduplicate while preserving order
    seen: set[str] = set()
    unique: list[str] = []
    for item in conflicts:
        if item not in seen:
            seen.add(item)
            unique.append(item)
    return unique


def label_for(component: ComponentRow) -> str:
    return f"{component.manufacturer} {component.model} ({component.category})"
