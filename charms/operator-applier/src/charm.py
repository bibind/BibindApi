"""Operator-applier charm."""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any

import yaml
from ops.charm import CharmBase, ActionEvent
from ops.main import main
from ops.model import ActiveStatus, BlockedStatus

try:  # pragma: no cover - lightkube may not be installed in tests
    from lightkube import Client
except Exception:  # pragma: no cover

    class Client:  # type: ignore
        def apply(self, *a: Any, **kw: Any) -> None:  # noqa: D401 - dummy
            pass


log = logging.getLogger(__name__)


class OperatorApplierCharm(CharmBase):
    """Apply CRDs and manifests using lightkube."""

    def __init__(self, *args: Any) -> None:
        super().__init__(*args)
        self.client = Client()
        self.framework.observe(self.on.install, self._reconcile)
        self.framework.observe(self.on.config_changed, self._reconcile)

    def _apply_path(self, path: Path) -> None:
        for mf in path.glob("*.yaml"):
            obj = yaml.safe_load(mf.read_text())
            self.client.apply(obj, field_manager="operator-applier", force=True)

    def _reconcile(self, _event: ActionEvent) -> None:
        root = Path(self.config["path"])
        if not root.exists():
            self.unit.status = BlockedStatus("path not found")
            return
        self._apply_path(root / "crds")
        self._apply_path(root / "manifests")
        self.unit.status = ActiveStatus("applied")

    # action stubs ------------------------------------------------------
    def _reapply_action(self, event: ActionEvent) -> None:
        self._reconcile(event)
        event.set_results({"result": "reapplied"})

    def _status_action(self, event: ActionEvent) -> None:
        event.set_results({"status": self.unit.status.message})

    def _purge_action(self, event: ActionEvent) -> None:
        event.set_results({"result": "purge not implemented"})


if __name__ == "__main__":  # pragma: no cover - main entry
    main(OperatorApplierCharm)
