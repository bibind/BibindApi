"""Simple HashiCorp Vault client wrapper."""

from __future__ import annotations

from typing import Any

import hvac


class VaultClient:
    """Wrapper around ``hvac.Client`` providing basic helpers."""

    def __init__(self, addr: str, token: str) -> None:
        self.client = hvac.Client(url=addr, token=token)

    def read_secret(self, path: str) -> dict[str, Any]:
        """Return the secret stored at ``path``."""
        result = self.client.secrets.kv.v2.read_secret_version(path=path)
        return result["data"]["data"]

    def write_secret(self, path: str, secret: dict[str, Any]) -> None:
        """Write ``secret`` at ``path``."""
        self.client.secrets.kv.v2.create_or_update_secret(path=path, secret=secret)


__all__ = ["VaultClient"]
