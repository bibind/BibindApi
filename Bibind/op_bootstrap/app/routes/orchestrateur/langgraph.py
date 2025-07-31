"""Langgraph routes."""

from fastapi import APIRouter
from fastapi.responses import JSONResponse

from app.services import orchestrator_service

router = APIRouter(prefix="/langgraph", tags=["orchestrateur"])


@router.post("/execute/simple")
async def execute_simple(payload: dict) -> JSONResponse:
    data = await orchestrator_service.execute_langgraph_simple(payload)
    return JSONResponse(status_code=200, content=data)


@router.post("/execute/custom")
async def execute_custom(payload: dict) -> JSONResponse:
    data = await orchestrator_service.execute_langgraph_custom(payload)
    return JSONResponse(status_code=200, content=data)


@router.get("/status/{workflow_id}")
async def get_status(workflow_id: int) -> JSONResponse:
    data = await orchestrator_service.langgraph_status(workflow_id)
    return JSONResponse(status_code=200, content=data)
