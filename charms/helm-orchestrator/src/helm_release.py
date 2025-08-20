"""Minimal HelmRelease wrapper for tests."""

from __future__ import annotations

from typing import Any, Dict


class HelmRelease:  # pragma: no cover - wrapper simplified for tests
    """Tiny stand-in for ops-lib-helm's HelmRelease."""

    def __init__(self, charm: Any, release_name: str, namespace: str) -> None:
        self.charm = charm
        self.release_name = release_name
        self.namespace = namespace
        self.last_install: Dict[str, Any] | None = None

    def install(
        self,
        chart: str,
        values: Dict[str, Any],
        version: str,
        atomic: bool,
        wait: bool,
        timeout: int,
    ) -> None:
        self.last_install = {
            "chart": chart,
            "values": values,
            "version": version,
            "atomic": atomic,
            "wait": wait,
            "timeout": timeout,
        }

    def rollback(self, revision: int | None) -> None:
        self.last_install = {"rollback": revision}

    def dry_run(self, chart: str, version: str, values: Dict[str, Any]) -> str:
        return "DRY-RUN"

    def diff(self, values: Dict[str, Any]) -> str:
        return "DIFF"

    def remove(self) -> None:
        self.last_install = None
