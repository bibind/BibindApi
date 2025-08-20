"""Unit tests for OperatorApplierCharm."""

from __future__ import annotations

import sys
from pathlib import Path

from ops.model import ActiveStatus, BlockedStatus
from ops.testing import Harness

sys.path.append(str(Path(__file__).resolve().parents[1]))
from charm import OperatorApplierCharm  # noqa: E402


def test_blocked_when_path_missing(tmp_path):
    harness = Harness(OperatorApplierCharm)
    harness.begin()
    harness.update_config({"path": str(tmp_path / "missing")})
    status = harness.model.unit.status
    assert isinstance(status, BlockedStatus)


def test_active_when_path_exists(tmp_path):
    resources = tmp_path / "res"
    (resources / "crds").mkdir(parents=True)
    (resources / "manifests").mkdir()
    (resources / "crds/crd.yaml").write_text("{}")
    (resources / "manifests/mf.yaml").write_text("{}")

    harness = Harness(OperatorApplierCharm)
    harness.begin()
    harness.update_config({"path": str(resources)})
    status = harness.model.unit.status
    assert isinstance(status, ActiveStatus)
