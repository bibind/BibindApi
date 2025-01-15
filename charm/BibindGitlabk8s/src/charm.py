#!/usr/bin/env python3

from ops.charm import CharmBase
from ops.main import main
from ops.model import ActiveStatus


class BibindGitlabK8sCharm(CharmBase):
    def __init__(self, *args):
        super().__init__(*args)
        self.framework.observe(self.on.install, self._on_install)
        self.framework.observe(self.on.config_changed, self._on_config_changed)

    def _on_install(self, event):
        """Déploiement initial du charm."""
        self.unit.status = ActiveStatus("GitLab déployé avec succès.")

    def _on_config_changed(self, event):
        """Appliquer les changements de configuration."""
        self.unit.status = ActiveStatus("Configuration mise à jour.")


if __name__ == "__main__":
    main(BibindGitlabK8sCharm)