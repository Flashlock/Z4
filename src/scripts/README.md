# Z4 package scripts

Run from `src/` (package root).

## Windows (existing)

Local toolchains under `../.tools/` when present:

```bash
..\.tools\python\python.exe -m venv .venv
.\.venv\Scripts\python.exe -m pip install -U pip
.\.venv\Scripts\python.exe -m pip install -e ".[dev]"
.\.venv\Scripts\python.exe scripts/export_openapi.py
.\.venv\Scripts\python.exe scripts/build_shim.py
```

Dev without Hub:

```bash
set AGENT_SERVICE_PORT=8787
.\.venv\Scripts\python.exe scripts/shim_entry.py
```

Windows package uses committed `manifest.json` (`bin/z4.exe`, windows-only platforms).

## Fedora / Linux

Use system Python ≥ 3.11 and Node (do **not** use Windows `../.tools`).

```bash
sudo dnf install python3 python3-devel nodejs npm

cd src
python3 -m venv .venv
.venv/bin/python -m pip install -U pip
.venv/bin/python -m pip install -e ".[dev]"

.venv/bin/python scripts/export_openapi.py
cd mfe && npm install && npm run build && cd ..
.venv/bin/python scripts/build_shim.py
# → bin/z4 and dist/linux/ (static linux-only manifest + Hub-ready tree)
```

Dev without Hub:

```bash
export AGENT_SERVICE_PORT=8787
.venv/bin/python scripts/shim_entry.py
# or: ./bin/z4
```

**Hub install on Fedora:** Add Agent → local folder → `src/dist/linux` (linux-only `manifest.json`, `bin/z4`). Ensure `dist/linux/.venv` exists (copied from `src/.venv` by `build_shim.py`).

Linux package identity is [`manifest.linux.json`](../manifest.linux.json) (`bin/z4`, `linux`/`x86_64` only). Windows `manifest.json` is unchanged.
