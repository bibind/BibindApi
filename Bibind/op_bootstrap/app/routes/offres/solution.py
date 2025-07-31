"""Solution routes."""

from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse

from app.schemas.solution import Solution, SolutionCreate
from app.services import solution_service

router = APIRouter(prefix="/solutions", tags=["solutions"])


@router.get("/", response_model=list[Solution])
async def list_solutions() -> list[Solution]:
    return await solution_service.list_solutions()


@router.post("/", response_model=Solution, status_code=status.HTTP_201_CREATED)
async def create_solution(payload: SolutionCreate) -> JSONResponse:
    sol = await solution_service.create_solution(payload)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=sol.dict())


@router.get("/{id}", response_model=Solution)
async def get_solution(id: int) -> Solution:
    sol = await solution_service.get_solution(id)
    if not sol:
        raise HTTPException(status_code=404, detail="Solution not found")
    return sol


@router.put("/{id}", response_model=Solution)
async def update_solution(id: int, payload: SolutionCreate) -> Solution:
    sol = await solution_service.update_solution(id, payload)
    if not sol:
        raise HTTPException(status_code=404, detail="Solution not found")
    return sol


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_solution(id: int) -> JSONResponse:
    success = await solution_service.delete_solution(id)
    if not success:
        raise HTTPException(status_code=404, detail="Solution not found")
    return JSONResponse(
        status_code=status.HTTP_204_NO_CONTENT, content={"detail": "deleted"}
    )
