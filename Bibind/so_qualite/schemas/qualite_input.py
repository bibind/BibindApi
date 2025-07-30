"""Pydantic schema for qualite input."""

from pydantic import BaseModel


class QualiteInput(BaseModel):
    """Input data required to run the qualite service."""

    data: str
