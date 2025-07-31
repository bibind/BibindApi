from app.schemas.projet import Projet, ProjetCreate


async def list_projets() -> list[Projet]:
    return [Projet(id=1, name="Projet1")]


async def create_projet(obj: ProjetCreate) -> Projet:
    return Projet(id=1, name=obj.name)


async def get_projet(projet_id: int) -> Projet | None:
    if projet_id == 1:
        return Projet(id=1, name="Projet1")
    return None


async def update_projet(projet_id: int, obj: ProjetCreate) -> Projet | None:
    if projet_id == 1:
        return Projet(id=1, name=obj.name)
    return None


async def delete_projet(projet_id: int) -> bool:
    return projet_id == 1
