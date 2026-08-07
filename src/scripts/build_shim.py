from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SHIM = ROOT / "scripts" / "shim_entry.py"
OUT_DIR = ROOT / "bin"


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    cmd = [
        sys.executable,
        "-m",
        "PyInstaller",
        "--noconfirm",
        "--clean",
        "--onefile",
        "--name",
        "z4",
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
    print(f"Built {OUT_DIR / 'z4.exe'}")


if __name__ == "__main__":
    main()
