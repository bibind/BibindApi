from pathlib import Path
from dotenv import load_dotenv
from pydantic import BaseSettings

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

    class Config:
        env_file = Path(__file__).resolve().parent.parent / '.env'
        case_sensitive = False

settings = Settings()

