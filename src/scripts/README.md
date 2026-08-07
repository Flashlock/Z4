# Z4 package scripts

Run from `src/` (package root).

## Local toolchains (workspace)

- Python: `../.tools/python/python.exe`
- Node/npm: `../.tools/node/`

## Create venv + install API deps

```bash
..\.tools\python\python.exe -m venv .venv
.\.venv\Scripts\python.exe -m pip install -U pip
.\.venv\Scripts\python.exe -m pip install -e ".[dev]"
```

## Export OpenAPI (required for Hub install)

```bash
.\.venv\Scripts\python.exe scripts/export_openapi.py
```

Writes `docs/openapi.json` from the live FastAPI app. Do not hand-edit that file.

## Dev without Hub

```bash
set AGENT_SERVICE_PORT=8787
.\.venv\Scripts\python.exe scripts/shim_entry.py
```

## Build stable Pantheon shim (`bin/z4.exe`)

```bash
.\.venv\Scripts\python.exe scripts/build_shim.py
```

Hub always starts `bin/z4.exe`. The shim delegates to `.venv` + `uvicorn --reload` against `api/`.

## Build MFE

```bash
cd mfe
$env:PATH = "..\..\.tools\node;" + $env:PATH
npm install
npm run build
```
