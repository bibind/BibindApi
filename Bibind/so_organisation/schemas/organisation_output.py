"""Pydantic schema for organisation output."""

from pydantic import BaseModel


class OrganisationOutput(BaseModel):
    """Result produced by the organisation service."""

    result: str
