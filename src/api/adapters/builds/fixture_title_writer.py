from __future__ import annotations

from api.domain.dtos import GoalView
from api.ports.build_recommender import RecommendedDraft


class FixtureTitleWriter:
    """Mock 'AI' titles derived from goal keywords + draft composition."""

    def title_for(self, goal: GoalView, draft: RecommendedDraft) -> str:
        text = (goal.text or "").lower()
        gpu = next((s for s in draft.slots if s.category == "gpu"), None)
        cpu = next((s for s in draft.slots if s.category == "cpu"), None)
        total = sum(s.listing.price_cents for s in draft.slots)

        if "edit" in text or "content" in text:
            vibe = "Creator-focused"
        elif "compete" in text or "esport" in text or "fps" in text:
            vibe = "Competitive"
        elif "quiet" in text or "office" in text:
            vibe = "Silent workstation"
        elif "budget" in text or "cheap" in text or total < 120000:
            vibe = "Value-first"
        else:
            vibe = "Balanced"

        gpu_bit = gpu.listing.component.model if gpu and gpu.listing.component else "Integrated"
        cpu_bit = cpu.listing.component.model if cpu and cpu.listing.component else "Flexible CPU"
        return f"{vibe}: {cpu_bit} + {gpu_bit}"
