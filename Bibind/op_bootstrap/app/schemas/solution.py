from pydantic import BaseModel


class SolutionBase(BaseModel):
    name: str


class SolutionCreate(SolutionBase):
    pass


class Solution(SolutionBase):
    id: int

    class Config:
        orm_mode = True
