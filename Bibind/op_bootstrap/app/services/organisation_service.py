from app.schemas.organisation import Organisation, OrganisationCreate


async def list_organisations() -> list[Organisation]:
    return [Organisation(id=1, name="Org1")]


async def create_organisation(org: OrganisationCreate) -> Organisation:
    return Organisation(id=1, name=org.name)


async def get_organisation(org_id: int) -> Organisation | None:
    if org_id == 1:
        return Organisation(id=1, name="Org1")
    return None


async def update_organisation(
    org_id: int, org: OrganisationCreate
) -> Organisation | None:
    if org_id == 1:
        return Organisation(id=1, name=org.name)
    return None


async def delete_organisation(org_id: int) -> bool:
    return org_id == 1
