"""Pydantic schema for organisation input."""

from pydantic import BaseModel


class OrganisationInput(BaseModel):
    """Input data required to run the organisation service."""

    data: str
