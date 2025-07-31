"""Offres routes."""

from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse

from app.schemas.offre import Offre, OffreCreate
from app.services import offre_service

router = APIRouter(prefix="/offres", tags=["offres"])


@router.get("/", response_model=list[Offre])
async def list_offres() -> list[Offre]:
    return await offre_service.list_offres()


@router.post("/", response_model=Offre, status_code=status.HTTP_201_CREATED)
async def create_offre(payload: OffreCreate) -> JSONResponse:
    off = await offre_service.create_offre(payload)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=off.dict())


@router.get("/{id}", response_model=Offre)
async def get_offre(id: int) -> Offre:
    off = await offre_service.get_offre(id)
    if not off:
        raise HTTPException(status_code=404, detail="Offre not found")
    return off


@router.put("/{id}", response_model=Offre)
async def update_offre(id: int, payload: OffreCreate) -> Offre:
    off = await offre_service.update_offre(id, payload)
    if not off:
        raise HTTPException(status_code=404, detail="Offre not found")
    return off


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_offre(id: int) -> JSONResponse:
    success = await offre_service.delete_offre(id)
    if not success:
        raise HTTPException(status_code=404, detail="Offre not found")
    return JSONResponse(
        status_code=status.HTTP_204_NO_CONTENT, content={"detail": "deleted"}
    )
