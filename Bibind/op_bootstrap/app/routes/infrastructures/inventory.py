"""Infrastructure inventory routes."""

from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

from app.schemas.infrastructure import Inventory, InventoryExport
from app.services import inventory_service

router = APIRouter(prefix="/infrastructures", tags=["infrastructures"])


@router.get("/{id}/inventory", response_model=Inventory)
async def get_inventory(id: int) -> Inventory:
    return await inventory_service.get_inventory(id)


@router.post("/{id}/inventory/export", response_model=InventoryExport)
async def export_inventory(id: int) -> InventoryExport:
    return await inventory_service.export_inventory(id)


@router.get("/{id}/tfstate")
async def get_tfstate(id: int) -> JSONResponse:
    data = await inventory_service.get_tfstate(id)
    return JSONResponse(status_code=status.HTTP_200_OK, content=data)
