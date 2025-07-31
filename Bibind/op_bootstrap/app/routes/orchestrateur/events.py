"""Events mapping routes."""

from fastapi import APIRouter
from fastapi.responses import JSONResponse

from app.services import orchestrator_service

router = APIRouter(prefix="/events", tags=["orchestrateur"])


@router.get("/types")
async def event_types() -> JSONResponse:
    data = await orchestrator_service.event_types()
    return JSONResponse(status_code=200, content={"types": data})


@router.get("/mapping")
async def event_mapping() -> JSONResponse:
    data = await orchestrator_service.event_mapping()
    return JSONResponse(status_code=200, content=data)


@router.post("/test")
async def test_event(payload: dict) -> JSONResponse:
    result = await orchestrator_service.test_event(payload)
    return JSONResponse(status_code=200, content={"result": result})
