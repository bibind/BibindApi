from pydantic import BaseModel


class ProjetBase(BaseModel):
    name: str


class ProjetCreate(ProjetBase):
    pass


class Projet(ProjetBase):
    id: int

    class Config:
        orm_mode = True
