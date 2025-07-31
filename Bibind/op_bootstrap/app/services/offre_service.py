from app.schemas.offre import Offre, OffreCreate


async def list_offres() -> list[Offre]:
    return [Offre(id=1, name="Offre1")]


async def create_offre(obj: OffreCreate) -> Offre:
    return Offre(id=1, name=obj.name)


async def get_offre(offre_id: int) -> Offre | None:
    if offre_id == 1:
        return Offre(id=1, name="Offre1")
    return None


async def update_offre(offre_id: int, obj: OffreCreate) -> Offre | None:
    if offre_id == 1:
        return Offre(id=1, name=obj.name)
    return None


async def delete_offre(offre_id: int) -> bool:
    return offre_id == 1
