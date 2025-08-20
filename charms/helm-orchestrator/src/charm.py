"""Helm orchestrator charm."""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any, Dict

import yaml
from ops.charm import CharmBase, ActionEvent
from ops.main import main
from ops.model import ActiveStatus, BlockedStatus, WaitingStatus

from .catalog import CatalogPolicy, CatalogViolation
from .validators import merge_values_validated
from .helm_release import HelmRelease

log = logging.getLogger(__name__)


class HelmOrchestratorCharm(CharmBase):
    """Charm orchestrating a Helm release.

    SECURITY: never log secrets.
    """

    def __init__(self, *args: Any) -> None:
        super().__init__(*args)
        self._helm = HelmRelease(
            self, self.config.get("release"), self.config.get("namespace")
        )
        self.framework.observe(self.on.install, self._reconcile)
        self.framework.observe(self.on.config_changed, self._reconcile)
        self.framework.observe(self.on.upgrade_action, self._upgrade_action)
        self.framework.observe(self.on.rollback_action, self._rollback_action)
        self.framework.observe(self.on.dry_run_action, self._dry_run_action)
        self.framework.observe(self.on.diff_action, self._diff_action)
        self.framework.observe(self.on.purge_action, self._purge_action)

    # ------------------------------------------------------------------
    # Helpers

    def _render_values(self) -> Dict[str, Any]:
        """Assemble Helm values from defaults, overrides and catalog policy."""

        base: Dict[str, Any] = {}
        policy = None
        if self.config.get("use-catalog"):
            policy = CatalogPolicy.from_path(Path(self.config["catalog-path"]))
            if not policy.allowed(self.config["chart"], self.config["version"]):
                raise CatalogViolation("chart or version not allowed")
            base = policy.defaults_for(self.config["chart"])
            allowed_keys = policy.allowed_keys(self.config["chart"])
        else:
            allowed_keys = None

        overrides = yaml.safe_load(self.config["values-override"] or "{}")
        merged = merge_values_validated(base, overrides, allowed_keys)
        # TODO: relation data injection
        return merged

    # ------------------------------------------------------------------
    # Hooks

    def _reconcile(self, _event: ActionEvent) -> None:
        """Main reconcile path."""

        try:
            values = self._render_values()
            self._helm.install(
                chart=self.config["chart"],
                values=values,
                version=self.config["version"],
                atomic=bool(self.config["atomic-upgrade"]),
                wait=True,
                timeout=int(self.config["wait-timeout"]),
            )
            self.unit.status = ActiveStatus(
                f"deployed {self.config['chart']}@{self.config['version']}"
            )
        except CatalogViolation as exc:
            self.unit.status = BlockedStatus(str(exc))
        except Exception as exc:  # noqa: BLE001 - surface helm failure
            log.exception("reconcile failed")
            self.unit.status = BlockedStatus(f"helm failed: {exc}")

    # ------------------------------------------------------------------
    # Actions (minimal stubs)

    def _upgrade_action(self, event: ActionEvent) -> None:
        self._reconcile(event)

    def _rollback_action(self, event: ActionEvent) -> None:
        revision = event.params.get("revision")
        self._helm.rollback(revision)
        event.set_results({"result": "rolled back"})

    def _dry_run_action(self, event: ActionEvent) -> None:
        diff = self._helm.dry_run(
            self.config["chart"], self.config["version"], self._render_values()
        )
        event.set_results({"diff": diff})

    def _diff_action(self, event: ActionEvent) -> None:
        event.set_results({"diff": self._helm.diff(self._render_values())})

    def _purge_action(self, event: ActionEvent) -> None:
        self._helm.remove()
        event.set_results({"result": "removed"})


if __name__ == "__main__":
    main(HelmOrchestratorCharm)
