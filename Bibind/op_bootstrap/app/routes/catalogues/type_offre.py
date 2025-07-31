"""Type offre catalogue routes."""

from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse

from app.schemas.type_offre import TypeOffre, TypeOffreCreate
from app.services import catalogue_service

router = APIRouter(prefix="/catalogues/type-offre", tags=["catalogues"])


@router.get("/", response_model=list[TypeOffre])
async def list_types() -> list[TypeOffre]:
    return await catalogue_service.list_type_offre()


@router.post("/", response_model=TypeOffre, status_code=status.HTTP_201_CREATED)
async def create_type(payload: TypeOffreCreate) -> JSONResponse:
    obj = await catalogue_service.create_type_offre(payload)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=obj.dict())


@router.get("/{id}", response_model=TypeOffre)
async def get_type(id: int) -> TypeOffre:
    obj = await catalogue_service.get_type_offre(id)
    if not obj:
        raise HTTPException(status_code=404, detail="Type not found")
    return obj


@router.put("/{id}", response_model=TypeOffre)
async def update_type(id: int, payload: TypeOffreCreate) -> TypeOffre:
    obj = await catalogue_service.update_type_offre(id, payload)
    if not obj:
        raise HTTPException(status_code=404, detail="Type not found")
    return obj


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_type(id: int) -> JSONResponse:
    success = await catalogue_service.delete_type_offre(id)
    if not success:
        raise HTTPException(status_code=404, detail="Type not found")
    return JSONResponse(
        status_code=status.HTTP_204_NO_CONTENT, content={"detail": "deleted"}
    )
