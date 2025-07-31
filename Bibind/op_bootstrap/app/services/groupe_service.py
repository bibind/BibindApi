from app.schemas.groupe import Groupe, GroupeCreate


async def list_groupes() -> list[Groupe]:
    return [Groupe(id=1, name="Groupe1")]


async def create_groupe(grp: GroupeCreate) -> Groupe:
    return Groupe(id=1, name=grp.name)


async def get_groupe(groupe_id: int) -> Groupe | None:
    if groupe_id == 1:
        return Groupe(id=1, name="Groupe1")
    return None


async def update_groupe(groupe_id: int, grp: GroupeCreate) -> Groupe | None:
    if groupe_id == 1:
        return Groupe(id=1, name=grp.name)
    return None


async def delete_groupe(groupe_id: int) -> bool:
    return groupe_id == 1
