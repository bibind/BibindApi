"""Pydantic schema for release input."""

from pydantic import BaseModel


class ReleaseInput(BaseModel):
    """Input data required to run the release service."""

    data: str
