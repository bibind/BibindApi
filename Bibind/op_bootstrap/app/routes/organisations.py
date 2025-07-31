"""Organisation routes."""

from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse

from app.schemas.organisation import Organisation, OrganisationCreate
from app.services import organisation_service

router = APIRouter(prefix="/organisations", tags=["organisations"])


@router.get("/", response_model=list[Organisation])
async def list_organisations() -> list[Organisation]:
    return await organisation_service.list_organisations()


@router.post("/", response_model=Organisation, status_code=status.HTTP_201_CREATED)
async def create_organisation(payload: OrganisationCreate) -> JSONResponse:
    org = await organisation_service.create_organisation(payload)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=org.dict())


@router.get("/{id}", response_model=Organisation)
async def get_organisation(id: int) -> Organisation:
    org = await organisation_service.get_organisation(id)
    if not org:
        raise HTTPException(status_code=404, detail="Organisation not found")
    return org


@router.put("/{id}", response_model=Organisation)
async def update_organisation(id: int, payload: OrganisationCreate) -> Organisation:
    org = await organisation_service.update_organisation(id, payload)
    if not org:
        raise HTTPException(status_code=404, detail="Organisation not found")
    return org


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_organisation(id: int) -> JSONResponse:
    success = await organisation_service.delete_organisation(id)
    if not success:
        raise HTTPException(status_code=404, detail="Organisation not found")
    return JSONResponse(
        status_code=status.HTTP_204_NO_CONTENT, content={"detail": "deleted"}
    )
