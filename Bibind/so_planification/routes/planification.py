"""API routes for the planification service."""

from fastapi import APIRouter
from schemas.planification_input import PlanificationInput
from schemas.planification_output import PlanificationOutput
from services.planification_agent import generate_planification

router = APIRouter(prefix="/planification", tags=["planification"])


@router.post("/", response_model=PlanificationOutput)
async def run_planification(payload: PlanificationInput) -> PlanificationOutput:
    """Trigger the planification workflow and return the result."""
    return await generate_planification(payload)
