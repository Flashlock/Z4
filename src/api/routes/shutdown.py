from __future__ import annotations

import os

from fastapi import APIRouter, BackgroundTasks

router = APIRouter(tags=["lifecycle"])


def _exit_process() -> None:
    os._exit(0)


@router.post("/api/v1/shutdown")
def shutdown(background_tasks: BackgroundTasks) -> dict[str, str]:
    # Hub may call this on instance delete; exit after response is sent.
    background_tasks.add_task(_exit_process)
    return {"status": "shutting_down"}
