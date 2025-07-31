from app.schemas.infrastructure import InventoryExport, Inventory


async def get_inventory(infra_id: int) -> Inventory:
    return Inventory(id=infra_id, name="inventory")


async def export_inventory(infra_id: int) -> InventoryExport:
    return InventoryExport(detail="exported", infra_id=infra_id)


async def get_tfstate(infra_id: int) -> dict:
    return {"id": infra_id, "tfstate": "{}"}
