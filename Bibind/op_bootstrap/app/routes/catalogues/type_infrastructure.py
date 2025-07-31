"""Type infrastructure catalogue routes."""

from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse

from app.schemas.type_infrastructure import TypeInfrastructure, TypeInfrastructureCreate
from app.services import catalogue_service

router = APIRouter(prefix="/catalogues/type-infrastructure", tags=["catalogues"])


@router.get("/", response_model=list[TypeInfrastructure])
async def list_types() -> list[TypeInfrastructure]:
    return await catalogue_service.list_type_infrastructure()


@router.post(
    "/", response_model=TypeInfrastructure, status_code=status.HTTP_201_CREATED
)
async def create_type(payload: TypeInfrastructureCreate) -> JSONResponse:
    obj = await catalogue_service.create_type_infrastructure(payload)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=obj.dict())


@router.get("/{id}", response_model=TypeInfrastructure)
async def get_type(id: int) -> TypeInfrastructure:
    obj = await catalogue_service.get_type_infrastructure(id)
    if not obj:
        raise HTTPException(status_code=404, detail="Type not found")
    return obj


@router.put("/{id}", response_model=TypeInfrastructure)
async def update_type(id: int, payload: TypeInfrastructureCreate) -> TypeInfrastructure:
    obj = await catalogue_service.update_type_infrastructure(id, payload)
    if not obj:
        raise HTTPException(status_code=404, detail="Type not found")
    return obj


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_type(id: int) -> JSONResponse:
    success = await catalogue_service.delete_type_infrastructure(id)
    if not success:
        raise HTTPException(status_code=404, detail="Type not found")
    return JSONResponse(
        status_code=status.HTTP_204_NO_CONTENT, content={"detail": "deleted"}
    )
