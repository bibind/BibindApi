"""Unit tests for HelmOrchestratorCharm."""

from __future__ import annotations

import sys
from pathlib import Path

from ops.model import ActiveStatus, BlockedStatus
from ops.testing import Harness

sys.path.append(str(Path(__file__).resolve().parents[1]))
from charm import HelmOrchestratorCharm  # noqa: E402


def test_blocked_when_chart_not_in_catalog(tmp_path):
    harness = Harness(HelmOrchestratorCharm)
    harness.begin()
    harness.update_config(
        {
            "chart": "unknown",
            "version": "1.0.0",
            "use-catalog": True,
            "catalog-path": "catalog/charts-example.yaml",
        }
    )
    status = harness.model.unit.status
    assert isinstance(status, BlockedStatus)


def test_active_when_chart_allowed():
    harness = Harness(HelmOrchestratorCharm)
    harness.begin()
    harness.update_config(
        {
            "chart": "odoo",
            "version": "23.1.1",
            "use-catalog": True,
            "catalog-path": "catalog/charts-example.yaml",
        }
    )
    status = harness.model.unit.status
    assert isinstance(status, ActiveStatus)
