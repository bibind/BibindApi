"""Pydantic schema for realisation output."""

from pydantic import BaseModel


class RealisationOutput(BaseModel):
    """Result produced by the realisation service."""

    result: str
