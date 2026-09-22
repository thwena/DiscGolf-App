from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Settings:
    environment: str
    secret_key: str
    bootstrap_token: str | None
    data_dir: Path
    static_dir: Path
    access_token_minutes: int
    trusted_hosts: tuple[str, ...]

    @classmethod
    def from_env(cls) -> Settings:
        environment = os.getenv("DGT_ENVIRONMENT", "production")
        secret_key = os.getenv("DGT_SECRET_KEY", "")
        if len(secret_key) < 32:
            raise RuntimeError("DGT_SECRET_KEY must contain at least 32 characters")
        bootstrap_token = os.getenv("DGT_BOOTSTRAP_TOKEN") or None
        token_minutes = int(os.getenv("DGT_ACCESS_TOKEN_MINUTES", "60"))
        if token_minutes < 5 or token_minutes > 1440:
            raise RuntimeError("DGT_ACCESS_TOKEN_MINUTES must be between 5 and 1440")
        trusted_hosts = tuple(
            host.strip()
            for host in os.getenv("DGT_TRUSTED_HOSTS", "localhost,127.0.0.1").split(",")
            if host.strip()
        )
        if not trusted_hosts:
            raise RuntimeError("DGT_TRUSTED_HOSTS must contain at least one host")
        return cls(
            environment=environment,
            secret_key=secret_key,
            bootstrap_token=bootstrap_token,
            data_dir=Path(os.getenv("DGT_DATA_DIR", "./data")).resolve(),
            static_dir=Path(os.getenv("DGT_STATIC_DIR", "./frontend/dist")).resolve(),
            access_token_minutes=token_minutes,
            trusted_hosts=trusted_hosts,
        )

    @property
    def database_path(self) -> Path:
        return self.data_dir / "disc-golf-tracker.sqlite3"
