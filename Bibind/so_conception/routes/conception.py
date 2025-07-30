"""API routes for the conception service."""

from fastapi import APIRouter
from schemas.conception_input import ConceptionInput
from schemas.conception_output import ConceptionOutput
from services.conception_agent import generate_conception

router = APIRouter(prefix="/conception", tags=["conception"])


@router.post("/", response_model=ConceptionOutput)
async def run_conception(payload: ConceptionInput) -> ConceptionOutput:
    """Trigger the conception workflow and return the result."""
    return await generate_conception(payload)
