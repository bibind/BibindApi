from pydantic import BaseModel


class OffreBase(BaseModel):
    name: str


class OffreCreate(OffreBase):
    pass


class Offre(OffreBase):
    id: int
    description: str | None = None

    class Config:
        orm_mode = True
