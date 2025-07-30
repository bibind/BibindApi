"""Pydantic schema for conception output."""

from pydantic import BaseModel


class ConceptionOutput(BaseModel):
    """Result produced by the conception service."""

    result: str
