"""Pydantic schema for planification input."""

from pydantic import BaseModel


class PlanificationInput(BaseModel):
    """Input data required to run the planification service."""

    data: str
