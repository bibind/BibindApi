"""API routes for the organisation service."""

from fastapi import APIRouter
from schemas.organisation_input import OrganisationInput
from schemas.organisation_output import OrganisationOutput
from services.organisation_agent import generate_organisation

router = APIRouter(prefix="/organisation", tags=["organisation"])


@router.post("/", response_model=OrganisationOutput)
async def run_organisation(payload: OrganisationInput) -> OrganisationOutput:
    """Trigger the organisation workflow and return the result."""
    return await generate_organisation(payload)
