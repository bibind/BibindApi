"""Projet routes."""

from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse

from app.schemas.projet import Projet, ProjetCreate
from app.services import project_service

router = APIRouter(prefix="/projets", tags=["projets"])


@router.get("/", response_model=list[Projet])
async def list_projets() -> list[Projet]:
    return await project_service.list_projets()


@router.post("/", response_model=Projet, status_code=status.HTTP_201_CREATED)
async def create_projet(payload: ProjetCreate) -> JSONResponse:
    proj = await project_service.create_projet(payload)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=proj.dict())


@router.get("/{id}", response_model=Projet)
async def get_projet(id: int) -> Projet:
    proj = await project_service.get_projet(id)
    if not proj:
        raise HTTPException(status_code=404, detail="Projet not found")
    return proj


@router.put("/{id}", response_model=Projet)
async def update_projet(id: int, payload: ProjetCreate) -> Projet:
    proj = await project_service.update_projet(id, payload)
    if not proj:
        raise HTTPException(status_code=404, detail="Projet not found")
    return proj


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_projet(id: int) -> JSONResponse:
    success = await project_service.delete_projet(id)
    if not success:
        raise HTTPException(status_code=404, detail="Projet not found")
    return JSONResponse(
        status_code=status.HTTP_204_NO_CONTENT, content={"detail": "deleted"}
    )
