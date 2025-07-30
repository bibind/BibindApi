"""Pydantic schema for qualite output."""

from pydantic import BaseModel


class QualiteOutput(BaseModel):
    """Result produced by the qualite service."""

    result: str
