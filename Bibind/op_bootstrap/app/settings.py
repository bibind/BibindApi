from pathlib import Path
from dotenv import load_dotenv
from pydantic import BaseSettings

from app.clients.vault_client import VaultClient

# Load environment variables from .env if present
load_dotenv(dotenv_path=Path(__file__).resolve().parent.parent / '.env')

class Settings(BaseSettings):
    """Application configuration loaded from environment variables."""

    env: str = "dev"
    database_url: str | None = None
    kafka_bootstrap_servers: str | None = None
    kafka_topic: str | None = None
    vault_addr: str | None = None
    vault_token: str | None = None
    keycloak_url: str | None = None
    keycloak_realm: str | None = None
    keycloak_client_id: str | None = None
    keycloak_client_secret: str | None = None
    secret_key: str = "changeme"
    access_token_expire_minutes: int = 30
    refresh_token_expire_minutes: int = 1440

    class Config:
        env_file = Path(__file__).resolve().parent.parent / '.env'
        case_sensitive = False

    def load_vault_secrets(self) -> None:
        """Populate settings from Vault when not in development."""
        if self.env == "dev" or not (self.vault_addr and self.vault_token):
            return

        client = VaultClient(self.vault_addr, self.vault_token)
        data = client.read_secret("bibind/op_bootstrap")
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)

settings = Settings()
settings.load_vault_secrets()

