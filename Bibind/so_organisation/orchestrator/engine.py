"""Engine that orchestrates the organisation step."""

from langgraph import Graph
from langgraph import Runner
from langgraph import Node


class OrganisationEngine:
    """Simple wrapper around LangGraph Runner."""

    def __init__(self, graph: Graph) -> None:
        self.runner = Runner(graph)

    def run(self) -> None:
        """Execute the organisation workflow."""
        self.runner.run()
