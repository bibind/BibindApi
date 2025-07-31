from pydantic import BaseModel


class TypeInfrastructureBase(BaseModel):
    name: str


class TypeInfrastructureCreate(TypeInfrastructureBase):
    pass


class TypeInfrastructure(TypeInfrastructureBase):
    id: int

    class Config:
        orm_mode = True
