from pydantic import BaseModel


class GroupeBase(BaseModel):
    name: str


class GroupeCreate(GroupeBase):
    pass


class Groupe(GroupeBase):
    id: int

    class Config:
        orm_mode = True
