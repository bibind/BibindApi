"""Pydantic schema for release output."""

from pydantic import BaseModel


class ReleaseOutput(BaseModel):
    """Result produced by the release service."""

    result: str
