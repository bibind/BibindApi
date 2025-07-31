from pydantic import BaseModel


class TypeOffreBase(BaseModel):
    name: str


class TypeOffreCreate(TypeOffreBase):
    pass


class TypeOffre(TypeOffreBase):
    id: int

    class Config:
        orm_mode = True
