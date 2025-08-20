"""Validation helpers."""

from __future__ import annotations

from copy import deepcopy
from typing import Any, Dict, Iterable, List

from .catalog import CatalogViolation


def merge_values_validated(
    base: Dict[str, Any], overrides: Dict[str, Any], allowed_keys: Iterable[str] | None
) -> Dict[str, Any]:
    """Merge two mappings while validating allowed keys.

    Args:
        base: Base values, typically from catalog defaults.
        overrides: User provided overrides.
        allowed_keys: Iterable of allowed dotted key paths.

    Returns:
        Merged dictionary of values.

    Raises:
        CatalogViolation: If an override key is not allowed.
    """

    allowed = set(allowed_keys or [])
    result = deepcopy(base)

    def _merge(prefix: List[str], dst: Dict[str, Any], src: Dict[str, Any]) -> None:
        for key, value in src.items():
            path = prefix + [key]
            dotted = ".".join(path)
            if allowed and dotted not in allowed:
                raise CatalogViolation(f"override key {dotted} not allowed")
            if isinstance(value, dict):
                node = dst.setdefault(key, {})
                if isinstance(node, dict):
                    _merge(path, node, value)
                else:
                    dst[key] = deepcopy(value)
            else:
                dst[key] = value

    _merge([], result, overrides)
    return result
