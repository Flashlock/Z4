"""
Stable Pantheon launcher entry.

Hub always starts bin/z4.exe. The shim resolves the package root and delegates
to the project venv's Python running uvicorn --reload (hot reload for Phase 1).
"""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path


def package_root_from_exe() -> Path:
    # PyInstaller one-file: sys.executable is bin/z4.exe
    exe = Path(sys.executable).resolve()
    if exe.name.lower() == "z4.exe" and exe.parent.name.lower() == "bin":
        return exe.parent.parent
    # Dev fallback when running as python scripts/shim_entry.py
    return Path(__file__).resolve().parents[1]


def resolve_python(root: Path) -> Path:
    venv_python = root / ".venv" / "Scripts" / "python.exe"
    if venv_python.exists():
        return venv_python
    return Path(sys.executable)


def main() -> int:
    root = package_root_from_exe()
    os.chdir(root)

    port = os.environ.get("AGENT_SERVICE_PORT", "8787")
    os.environ.setdefault("PANTHEON_INSTANCE_ID", "local-dev")
    os.environ.setdefault("PANTHEON_PROXY_SECRET", "dev-proxy-secret")

    python = resolve_python(root)
    env = os.environ.copy()
    existing = env.get("PYTHONPATH", "")
    env["PYTHONPATH"] = str(root) if not existing else f"{root}{os.pathsep}{existing}"

    cmd = [
        str(python),
        "-m",
        "uvicorn",
        "api.main:app",
        "--host",
        "0.0.0.0",
        "--port",
        str(port),
        "--reload",
        "--reload-dir",
        str(root / "api"),
    ]
    return subprocess.call(cmd, cwd=str(root), env=env)


if __name__ == "__main__":
    raise SystemExit(main())
