from app.schemas.type_infrastructure import TypeInfrastructure, TypeInfrastructureCreate
from app.schemas.type_offre import TypeOffre, TypeOffreCreate


async def list_type_infrastructure() -> list[TypeInfrastructure]:
    return [TypeInfrastructure(id=1, name="VM")]


async def create_type_infrastructure(
    obj: TypeInfrastructureCreate,
) -> TypeInfrastructure:
    return TypeInfrastructure(id=1, name=obj.name)


async def get_type_infrastructure(type_id: int) -> TypeInfrastructure | None:
    if type_id == 1:
        return TypeInfrastructure(id=1, name="VM")
    return None


async def update_type_infrastructure(
    type_id: int, obj: TypeInfrastructureCreate
) -> TypeInfrastructure | None:
    if type_id == 1:
        return TypeInfrastructure(id=1, name=obj.name)
    return None


async def delete_type_infrastructure(type_id: int) -> bool:
    return type_id == 1


async def list_type_offre() -> list[TypeOffre]:
    return [TypeOffre(id=1, name="SaaS")]


async def create_type_offre(obj: TypeOffreCreate) -> TypeOffre:
    return TypeOffre(id=1, name=obj.name)


async def get_type_offre(type_id: int) -> TypeOffre | None:
    if type_id == 1:
        return TypeOffre(id=1, name="SaaS")
    return None


async def update_type_offre(type_id: int, obj: TypeOffreCreate) -> TypeOffre | None:
    if type_id == 1:
        return TypeOffre(id=1, name=obj.name)
    return None


async def delete_type_offre(type_id: int) -> bool:
    return type_id == 1
