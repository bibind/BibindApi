"""API routes for the qualite service."""

from fastapi import APIRouter
from schemas.qualite_input import QualiteInput
from schemas.qualite_output import QualiteOutput
from services.qualite_agent import generate_qualite

router = APIRouter(prefix="/qualite", tags=["qualite"])


@router.post("/", response_model=QualiteOutput)
async def run_qualite(payload: QualiteInput) -> QualiteOutput:
    """Trigger the qualite workflow and return the result."""
    return await generate_qualite(payload)
