from app.schemas.solution import Solution, SolutionCreate


async def list_solutions() -> list[Solution]:
    return [Solution(id=1, name="Solution1")]


async def create_solution(obj: SolutionCreate) -> Solution:
    return Solution(id=1, name=obj.name)


async def get_solution(solution_id: int) -> Solution | None:
    if solution_id == 1:
        return Solution(id=1, name="Solution1")
    return None


async def update_solution(solution_id: int, obj: SolutionCreate) -> Solution | None:
    if solution_id == 1:
        return Solution(id=1, name=obj.name)
    return None


async def delete_solution(solution_id: int) -> bool:
    return solution_id == 1
