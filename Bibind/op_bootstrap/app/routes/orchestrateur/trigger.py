"""Trigger orchestrator routes."""

from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

from app.services import orchestrator_service

router = APIRouter(prefix="/trigger", tags=["orchestrateur"])


@router.post("/{so_name}")
async def trigger_so(so_name: str, payload: dict) -> JSONResponse:
    result = await orchestrator_service.trigger_so(so_name, payload)
    return JSONResponse(
        status_code=status.HTTP_202_ACCEPTED, content={"result": result}
    )


@router.get("/list")
async def list_triggers() -> JSONResponse:
    data = await orchestrator_service.list_triggers()
    return JSONResponse(status_code=200, content={"triggers": data})
