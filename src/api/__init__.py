"""Z4 FastAPI agent package."""

from api.config import load_manifest

__version__ = str(load_manifest()["version"])
