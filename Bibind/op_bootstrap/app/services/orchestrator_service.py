from typing import List, Dict


async def trigger_offre(data: Dict) -> str:
    return "triggered"


async def get_status(task_id: int) -> Dict:
    return {"task_id": task_id, "status": "running"}


async def trigger_so(so_name: str, payload: Dict) -> str:
    return f"triggered {so_name}"


async def list_triggers() -> List[str]:
    return ["so_conception", "so_planification"]


async def event_types() -> List[str]:
    return ["type1", "type2"]


async def event_mapping() -> Dict[str, str]:
    return {"type1": "so_conception"}


async def test_event(data: Dict) -> str:
    return "ok"


async def execute_langgraph_simple(data: Dict) -> Dict:
    return {"workflow_id": 1}


async def execute_langgraph_custom(data: Dict) -> Dict:
    return {"workflow_id": 2}


async def langgraph_status(workflow_id: int) -> Dict:
    return {"workflow_id": workflow_id, "status": "done"}


async def approve_event(event_id: int) -> bool:
    return event_id == 1


async def reject_event(event_id: int) -> bool:
    return event_id == 1


async def pending_events() -> List[int]:
    return [1, 2]
