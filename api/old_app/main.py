#!/usr/bin/env python3
"""
Point d'entrée principal de l'application API de BindingAPI.

Author  : Houssou Audrey-Roch
Société : Bibind
Email   : audreyroch.houssou@bibind.com

Description :
Ce fichier initialise l'application FastAPI, configure les routes nécessaires,
et s'assure de la gestion des connexions à la base de données.
"""

# Imports système
import logging

# Imports des bibliothèques tierces
from fastapi import FastAPI

# Imports internes
from app.db.database import init_db, close_db
from app.routers import auth
from app.core.config import settings

# Configuration du logger
logging.basicConfig(level=settings.LOG_LEVEL.upper())
logger = logging.getLogger(settings.APP_NAME)


# Fonction pour créer l'application FastAPI
def create_app() -> FastAPI:
    """
    Initialise l'application FastAPI avec les routes et événements.

    Returns:
        FastAPI: L'instance de l'application FastAPI configurée.
    """
    app = FastAPI(
        title=settings.APP_NAME,
        description="API de Bibind pour l'authentification et autres fonctionnalités.",
        version="1.0.0",
    )
    logger.info("Application FastAPI - Initialisation des routes et événements...")

    # Inclusion des routes
    app.include_router(auth.router, prefix="/auth", tags=["Authentification"])

    # Événements à l'ouverture et à la fermeture de l'application
    @app.on_event("startup")
    async def startup():
        logger.info("Démarrage de l'application : initialisation de la base de données.")
        await init_db()

    @app.on_event("shutdown")
    async def shutdown():
        logger.info("Fermeture de l'application : fermeture de la base de données.")
        await close_db()

    return app


# Point d'entrée principal
app = create_app()