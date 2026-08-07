from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path
from typing import Any

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


def package_root() -> Path:
    """Pantheon package root (directory containing manifest.json)."""
    return Path(__file__).resolve().parents[1]


@lru_cache
def load_manifest() -> dict[str, Any]:
    path = package_root() / "manifest.json"
    return json.loads(path.read_text(encoding="utf-8"))


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=None, extra="ignore", populate_by_name=True)

    pantheon_host_uri: str = Field(default="", validation_alias="PANTHEON_HOST_URI")
    pantheon_instance_token: str = Field(default="", validation_alias="PANTHEON_INSTANCE_TOKEN")
    pantheon_instance_id: str = Field(default="local-dev", validation_alias="PANTHEON_INSTANCE_ID")
    pantheon_instance_nickname: str = Field(default="z4-dev", validation_alias="PANTHEON_INSTANCE_NICKNAME")
    agent_service_port: int = Field(default=8787, validation_alias="AGENT_SERVICE_PORT")
    pantheon_proxy_secret: str = Field(default="dev-proxy-secret", validation_alias="PANTHEON_PROXY_SECRET")
    database_path: str = Field(default="", validation_alias="Z4_DATABASE_PATH")

    @property
    def agent_id(self) -> str:
        return str(load_manifest()["agentId"])

    @property
    def package_version(self) -> str:
        return str(load_manifest()["version"])

    @property
    def hub_base_url(self) -> str:
        uri = self.pantheon_host_uri
        if uri.startswith("pantheon+"):
            return uri.removeprefix("pantheon+")
        return uri

    @property
    def sqlite_path(self) -> Path:
        if self.database_path:
            return Path(self.database_path)
        return package_root() / "data" / "z4.sqlite3"


@lru_cache
def get_settings() -> Settings:
    return Settings()
