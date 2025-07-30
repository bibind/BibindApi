"""API routes for the realisation service."""

from fastapi import APIRouter
from schemas.realisation_input import RealisationInput
from schemas.realisation_output import RealisationOutput
from services.realisation_agent import generate_realisation

router = APIRouter(prefix="/realisation", tags=["realisation"])


@router.post("/", response_model=RealisationOutput)
async def run_realisation(payload: RealisationInput) -> RealisationOutput:
    """Trigger the realisation workflow and return the result."""
    return await generate_realisation(payload)
