from typing import List


async def approve(event_id: int) -> bool:
    return event_id == 1


async def reject(event_id: int) -> bool:
    return event_id == 1


async def pending() -> List[int]:
    return [1]
