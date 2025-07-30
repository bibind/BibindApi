"""Logic to generate planification output using LLM/LangChain."""

from schemas.planification_input import PlanificationInput
from schemas.planification_output import PlanificationOutput


async def generate_planification(payload: PlanificationInput) -> PlanificationOutput:
    """Stub implementation that returns a simple response."""
    # TODO: integrate LangChain/Ollama logic here
    return PlanificationOutput(result="Planification generated")
