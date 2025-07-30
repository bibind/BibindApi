"""Pydantic schema for realisation input."""

from pydantic import BaseModel


class RealisationInput(BaseModel):
    """Input data required to run the realisation service."""

    data: str
