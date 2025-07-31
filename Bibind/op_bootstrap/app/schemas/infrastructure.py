from pydantic import BaseModel


class InfrastructureBase(BaseModel):
    name: str


class InfrastructureCreate(InfrastructureBase):
    pass


class Infrastructure(InfrastructureBase):
    id: int

    class Config:
        orm_mode = True


class Inventory(BaseModel):
    id: int
    name: str


class InventoryExport(BaseModel):
    infra_id: int
    detail: str
