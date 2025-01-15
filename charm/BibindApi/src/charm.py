from ops.charm import CharmBase
from ops.main import main
from ops.model import ActiveStatus, MaintenanceStatus


class BindingAPICharm(CharmBase):
    def __init__(self, *args):
        super().__init__(*args)

        # Observateurs d'événements
        self.framework.observe(self.on.install, self._on_install)
        self.framework.observe(self.on.upgrade_charm, self._on_upgrade_charm)

    # Gestion de l'installation
    def _on_install(self, event):
        self.unit.status = MaintenanceStatus("Installe BindingAPI...")
        # Déployer les conteneurs associés
        self._deploy_backend()
        self._deploy_frontend()
        self.unit.status = ActiveStatus("BindingAPI déployé avec succès")

    def _on_upgrade_charm(self, event):
        self.unit.status = MaintenanceStatus("Mise-à-jour...")

    def _deploy_backend(self):
        # Logique de déploiement backend
        self.unit.status = MaintenanceStatus("Déploiement du backend...")

    def _deploy_frontend(self):
        # Logique de déploiement frontend
        self.unit.status = MaintenanceStatus("Déploiement du frontend...")


main(BindingAPICharm)