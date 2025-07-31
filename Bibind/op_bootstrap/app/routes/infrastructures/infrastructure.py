"""Infrastructure routes."""

from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse

from app.schemas.infrastructure import Infrastructure, InfrastructureCreate
from app.services import infrastructure_service

router = APIRouter(prefix="/infrastructures", tags=["infrastructures"])


@router.get("/", response_model=list[Infrastructure])
async def list_infrastructures() -> list[Infrastructure]:
    return await infrastructure_service.list_infrastructures()


@router.post("/", response_model=Infrastructure, status_code=status.HTTP_201_CREATED)
async def create_infrastructure(payload: InfrastructureCreate) -> JSONResponse:
    infra = await infrastructure_service.create_infrastructure(payload)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=infra.dict())


@router.get("/{id}", response_model=Infrastructure)
async def get_infrastructure(id: int) -> Infrastructure:
    infra = await infrastructure_service.get_infrastructure(id)
    if not infra:
        raise HTTPException(status_code=404, detail="Infrastructure not found")
    return infra


@router.put("/{id}", response_model=Infrastructure)
async def update_infrastructure(
    id: int, payload: InfrastructureCreate
) -> Infrastructure:
    infra = await infrastructure_service.update_infrastructure(id, payload)
    if not infra:
        raise HTTPException(status_code=404, detail="Infrastructure not found")
    return infra


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_infrastructure(id: int) -> JSONResponse:
    success = await infrastructure_service.delete_infrastructure(id)
    if not success:
        raise HTTPException(status_code=404, detail="Infrastructure not found")
    return JSONResponse(
        status_code=status.HTTP_204_NO_CONTENT, content={"detail": "deleted"}
    )
