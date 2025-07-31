from typing import List


async def get_status(infra_id: int) -> dict:
    return {"infra_id": infra_id, "status": "ok"}


async def get_logs(infra_id: int) -> List[str]:
    return [f"log line for {infra_id}"]


async def get_alerts() -> List[str]:
    return ["alert1", "alert2"]
