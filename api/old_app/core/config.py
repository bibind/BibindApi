# config.py
"""
Configuration du projet BindingAPI
Author  : Houssou Audrey-Roch
Société : Bibind
Email   : audreyroch.houssou@bibind.com
"""

from decouple import config

# Charge explicitement le fichier env.local



class Settings:
    # ========================================
    # Application
    # ========================================
    APP_NAME: str = config("APP_NAME", default="BindingAPI")
    APP_ENV: str = config("APP_ENV", default="production")
    APP_PORT: int = config("APP_PORT", cast=int, default=8000)
    LOG_LEVEL: str = config("LOG_LEVEL", default="info")

    # ========================================
    # Base de données
    # ========================================
    TEST:str = config("TEST")
    POSTGRES_USER: str = config("POSTGRES_USER", default="user")
    POSTGRES_PASSWORD: str = config("POSTGRES_PASSWORD", default="password")
    POSTGRES_DB: str = config("POSTGRES_DB", default="bibindapi_db")
    POSTGRES_PORT: int = config("POSTGRES_PORT", cast=int, default=5432)
    DATABASE_URL: str = config(
        "DATABASE_URL",
        default=f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@localhost:{POSTGRES_PORT}/{POSTGRES_DB}",
    )

    # ========================================
    # Sécurité et Authentification
    # ========================================
    SECRET_KEY: str = config("SECRET_KEY", default="strong_secret_key")
    HYDRA_ISSUER_URL: str = config("HYDRA_ISSUER_URL", default="http://localhost:4444")
    OIDC_AUTHORIZATION_URL: str = config("OIDC_AUTHORIZATION_URL", default="http://localhost:4444")
    OIDC_TOKEN_URL: str = config("OIDC_TOKEN_URL")
    OIDC_CLIENT_ID: str = config("OIDC_CLIENT_ID", default="client_id")
    OIDC_CLIENT_SECRET: str = config("OIDC_CLIENT_SECRET", default="client_secret")
    OIDC_REDIRECT_URI: str = config("OIDC_REDIRECT_URI")

    # ========================================
    # GitLab Configuration
    # ========================================
    GITLAB_HOSTNAME: str = config("GITLAB_HOSTNAME", default="http://localhost:8080")
    GITLAB_API_TOKEN_FILE: str = config("GITLAB_API_TOKEN_FILE", default="secrets/gitlab_token_local")

    # ========================================
    # AWX Parameters
    # ========================================
    AWX_HOSTNAME: str = config("AWX_HOSTNAME", default="http://localhost:8052")
    AWX_USERNAME: str = config("AWX_USERNAME", default="admin")
    AWX_PASSWORD_FILE: str = config("AWX_PASSWORD_FILE", default="secrets/awx_password_local")

    # ========================================
    # Frontend Configuration
    # ========================================
    VITE_API_URL: str = config("VITE_API_URL", default="http://localhost:8000")
    FRONTEND_DEV_PORT: int = config("FRONTEND_DEV_PORT", default=8081, cast=int)

    # ========================================
    # Specific Ports
    # ========================================
    ODOO_PORT: int = config("ODOO_PORT", cast=int, default=8069)
    HYDRA_PUBLIC_PORT: int = config("HYDRA_PUBLIC_PORT", cast=int, default=4444)
    HYDRA_ADMIN_PORT: int = config("HYDRA_ADMIN_PORT", cast=int, default=4445)
    KRATOS_PUBLIC_PORT: int = config("KRATOS_PUBLIC_PORT", cast=int, default=4433)
    KRATOS_ADMIN_PORT: int = config("KRATOS_ADMIN_PORT", cast=int, default=4434)


# Instance globale des paramètres pour être utilisée dans tout le projet
settings = Settings()