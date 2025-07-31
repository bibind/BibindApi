"""Monitoring routes."""

from fastapi import APIRouter
from fastapi.responses import JSONResponse

from app.services import monitoring_service

router = APIRouter(tags=["monitoring"])  # prefix added in paths


@router.get("/monitoring/{infra_id}/status")
async def status(infra_id: int) -> JSONResponse:
    data = await monitoring_service.get_status(infra_id)
    return JSONResponse(status_code=200, content=data)


@router.get("/monitoring/{infra_id}/logs")
async def logs(infra_id: int) -> JSONResponse:
    data = await monitoring_service.get_logs(infra_id)
    return JSONResponse(status_code=200, content={"logs": data})


@router.get("/monitoring/alerts")
async def alerts() -> JSONResponse:
    data = await monitoring_service.get_alerts()
    return JSONResponse(status_code=200, content={"alerts": data})
