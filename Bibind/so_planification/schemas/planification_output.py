"""Pydantic schema for planification output."""

from pydantic import BaseModel


class PlanificationOutput(BaseModel):
    """Result produced by the planification service."""

    result: str
