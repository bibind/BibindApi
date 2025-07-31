"""Groupe routes."""

from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse

from app.schemas.groupe import Groupe, GroupeCreate
from app.services import groupe_service

router = APIRouter(prefix="/groupes", tags=["groupes"])


@router.get("/", response_model=list[Groupe])
async def list_groupes() -> list[Groupe]:
    return await groupe_service.list_groupes()


@router.post("/", response_model=Groupe, status_code=status.HTTP_201_CREATED)
async def create_groupe(payload: GroupeCreate) -> JSONResponse:
    grp = await groupe_service.create_groupe(payload)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=grp.dict())


@router.get("/{id}", response_model=Groupe)
async def get_groupe(id: int) -> Groupe:
    grp = await groupe_service.get_groupe(id)
    if not grp:
        raise HTTPException(status_code=404, detail="Groupe not found")
    return grp


@router.put("/{id}", response_model=Groupe)
async def update_groupe(id: int, payload: GroupeCreate) -> Groupe:
    grp = await groupe_service.update_groupe(id, payload)
    if not grp:
        raise HTTPException(status_code=404, detail="Groupe not found")
    return grp


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_groupe(id: int) -> JSONResponse:
    success = await groupe_service.delete_groupe(id)
    if not success:
        raise HTTPException(status_code=404, detail="Groupe not found")
    return JSONResponse(
        status_code=status.HTTP_204_NO_CONTENT, content={"detail": "deleted"}
    )
