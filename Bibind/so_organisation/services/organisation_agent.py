"""Logic to generate organisation output using LLM/LangChain."""

from schemas.organisation_input import OrganisationInput
from schemas.organisation_output import OrganisationOutput


async def generate_organisation(payload: OrganisationInput) -> OrganisationOutput:
    """Stub implementation that returns a simple response."""
    # TODO: integrate LangChain/Ollama logic here
    return OrganisationOutput(result="Organisation generated")
