from app.schemas.infrastructure import Infrastructure, InfrastructureCreate


async def list_infrastructures() -> list[Infrastructure]:
    return [Infrastructure(id=1, name="infra1")]


async def create_infrastructure(obj: InfrastructureCreate) -> Infrastructure:
    return Infrastructure(id=1, name=obj.name)


async def get_infrastructure(infra_id: int) -> Infrastructure | None:
    if infra_id == 1:
        return Infrastructure(id=1, name="infra1")
    return None


async def update_infrastructure(
    infra_id: int, obj: InfrastructureCreate
) -> Infrastructure | None:
    if infra_id == 1:
        return Infrastructure(id=1, name=obj.name)
    return None


async def delete_infrastructure(infra_id: int) -> bool:
    return infra_id == 1
