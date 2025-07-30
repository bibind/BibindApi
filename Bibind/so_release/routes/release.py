"""API routes for the release service."""

from fastapi import APIRouter
from schemas.release_input import ReleaseInput
from schemas.release_output import ReleaseOutput
from services.release_agent import generate_release

router = APIRouter(prefix="/release", tags=["release"])


@router.post("/", response_model=ReleaseOutput)
async def run_release(payload: ReleaseInput) -> ReleaseOutput:
    """Trigger the release workflow and return the result."""
    return await generate_release(payload)
