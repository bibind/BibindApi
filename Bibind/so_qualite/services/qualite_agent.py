"""Logic to generate qualite output using LLM/LangChain."""

from schemas.qualite_input import QualiteInput
from schemas.qualite_output import QualiteOutput


async def generate_qualite(payload: QualiteInput) -> QualiteOutput:
    """Stub implementation that returns a simple response."""
    # TODO: integrate LangChain/Ollama logic here
    return QualiteOutput(result="Qualite generated")
