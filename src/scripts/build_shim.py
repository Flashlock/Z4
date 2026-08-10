from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SHIM = ROOT / "scripts" / "shim_entry.py"
OUT_DIR = ROOT / "bin"


def shim_binary_name() -> str:
    return "z4.exe" if sys.platform == "win32" else "z4"


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    name = "z4"
    cmd = [
        sys.executable,
        "-m",
        "PyInstaller",
        "--noconfirm",
        "--clean",
        "--onefile",
        "--name",
        name,
        "--distpath",
        str(OUT_DIR),
        "--workpath",
        str(ROOT / ".build" / "shim" / "work"),
        "--specpath",
        str(ROOT / ".build" / "shim"),
        str(SHIM),
    ]
    print(" ".join(cmd))
    subprocess.check_call(cmd, cwd=str(ROOT))

    built = OUT_DIR / shim_binary_name()
    if not built.is_file():
        # PyInstaller on some platforms may omit .exe in the name we requested.
        alt = OUT_DIR / name
        if alt.is_file():
            built = alt
    if not built.is_file():
        raise SystemExit(f"expected shim binary missing under {OUT_DIR}")

    if sys.platform != "win32":
        mode = built.stat().st_mode
        os.chmod(built, mode | 0o111)

    print(f"Built {built}")

    if sys.platform != "win32":
        assemble_linux_package(built)


def assemble_linux_package(shim: Path) -> None:
    """Write a Linux-only Hub package tree under dist/linux/ (static linux manifest)."""
    dest = ROOT / "dist" / "linux"
    if dest.exists():
        shutil.rmtree(dest)
    dest.mkdir(parents=True)

    shutil.copy2(ROOT / "manifest.linux.json", dest / "manifest.json")

    for rel in ("api", "docs", "scripts"):
        src = ROOT / rel
        if src.exists():
            shutil.copytree(src, dest / rel, dirs_exist_ok=True)

    mfe = ROOT / "dist_mfe"
    if mfe.is_dir():
        shutil.copytree(mfe, dest / "dist_mfe")

    (dest / "bin").mkdir(parents=True, exist_ok=True)
    shutil.copy2(shim, dest / "bin" / "z4")
    os.chmod(dest / "bin" / "z4", (dest / "bin" / "z4").stat().st_mode | 0o111)

    # Phase-1 shim expects a venv beside the package root.
    venv = ROOT / ".venv"
    if venv.is_dir():
        shutil.copytree(venv, dest / ".venv", symlinks=True)

    for extra in ("pyproject.toml", "README.md"):
        src = ROOT / extra
        if src.is_file():
            shutil.copy2(src, dest / extra)

    print(f"Linux package ready: {dest}")
    print("Hub → Add Agent → local folder → dist/linux")


if __name__ == "__main__":
    main()
