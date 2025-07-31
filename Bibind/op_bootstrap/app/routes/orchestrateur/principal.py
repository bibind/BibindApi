"""Orchestrateur principal routes."""

from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

from app.services import orchestrator_service

router = APIRouter(prefix="/orchestrateur", tags=["orchestrateur"])


@router.post("/trigger-offre")
async def trigger_offre(payload: dict) -> JSONResponse:
    result = await orchestrator_service.trigger_offre(payload)
    return JSONResponse(
        status_code=status.HTTP_202_ACCEPTED, content={"result": result}
    )


@router.get("/status/{id}")
async def status(id: int) -> JSONResponse:
    data = await orchestrator_service.get_status(id)
    return JSONResponse(status_code=200, content=data)
