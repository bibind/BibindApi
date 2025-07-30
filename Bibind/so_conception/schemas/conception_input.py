"""Pydantic schema for conception input."""

from pydantic import BaseModel


class ConceptionInput(BaseModel):
    """Input data required to run the conception service."""

    data: str
