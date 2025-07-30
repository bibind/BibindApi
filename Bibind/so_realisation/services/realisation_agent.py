"""Logic to generate realisation output using LLM/LangChain."""

from schemas.realisation_input import RealisationInput
from schemas.realisation_output import RealisationOutput


async def generate_realisation(payload: RealisationInput) -> RealisationOutput:
    """Stub implementation that returns a simple response."""
    # TODO: integrate LangChain/Ollama logic here
    return RealisationOutput(result="Realisation generated")
