"""Simplified Keycloak client wrapper."""

from __future__ import annotations

from typing import Any, Dict

from keycloak import KeycloakOpenID

from app.settings import settings


class KeycloakClient:
    """Wrapper around ``python-keycloak`` to interact with Keycloak."""

    def __init__(self) -> None:
        self._openid = KeycloakOpenID(
            server_url=settings.keycloak_url,
            realm_name=settings.keycloak_realm,
            client_id=settings.keycloak_client_id,
            client_secret_key=settings.keycloak_client_secret,
        )

    def login(self, username: str, password: str) -> Dict[str, Any]:
        return self._openid.token(username, password)

    def refresh(self, refresh_token: str) -> Dict[str, Any]:
        return self._openid.refresh_token(refresh_token)

    def userinfo(self, access_token: str) -> Dict[str, Any]:
        return self._openid.userinfo(access_token)
