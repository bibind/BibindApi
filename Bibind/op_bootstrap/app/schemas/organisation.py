from pydantic import BaseModel


class OrganisationBase(BaseModel):
    name: str


class OrganisationCreate(OrganisationBase):
    pass


class Organisation(OrganisationBase):
    id: int

    class Config:
        orm_mode = True
