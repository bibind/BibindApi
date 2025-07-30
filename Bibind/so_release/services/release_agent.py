"""Logic to generate release output using LLM/LangChain."""

from schemas.release_input import ReleaseInput
from schemas.release_output import ReleaseOutput


async def generate_release(payload: ReleaseInput) -> ReleaseOutput:
    """Stub implementation that returns a simple response."""
    # TODO: integrate LangChain/Ollama logic here
    return ReleaseOutput(result="Release generated")
