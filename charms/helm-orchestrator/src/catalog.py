"""Catalog policy utilities."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List

import yaml


class CatalogViolation(Exception):
    """Raised when catalog validation fails."""


@dataclass
class _ChartEntry:
    name: str
    source: str
    versions: List[str]
    defaults: Dict[str, Any]
    allowed_keys: List[str]


class CatalogPolicy:
    """Simple in-memory representation of the catalog."""

    def __init__(self, charts: Dict[str, _ChartEntry]):
        self._charts = charts

    @classmethod
    def from_path(cls, path: Path) -> "CatalogPolicy":
        data = yaml.safe_load(path.read_text())
        charts: Dict[str, _ChartEntry] = {}
        for entry in data.get("charts", []):
            charts[entry["name"]] = _ChartEntry(
                name=entry["name"],
                source=entry.get("source", ""),
                versions=entry.get("versions", []),
                defaults=entry.get("defaults", {}),
                allowed_keys=entry.get("values_schema", {}).get("allowed_keys", []),
            )
        return cls(charts)

    def allowed(self, chart: str, version: str) -> bool:
        entry = self._charts.get(chart)
        return bool(entry and version in entry.versions)

    def defaults_for(self, chart: str) -> Dict[str, Any]:
        entry = self._charts.get(chart)
        return dict(entry.defaults) if entry else {}

    def allowed_keys(self, chart: str) -> List[str]:
        entry = self._charts.get(chart)
        return list(entry.allowed_keys) if entry else []
