"""Engine that orchestrates the realisation step."""

from langgraph import Graph
from langgraph import Runner
from langgraph import Node


class RealisationEngine:
    """Simple wrapper around LangGraph Runner."""

    def __init__(self, graph: Graph) -> None:
        self.runner = Runner(graph)

    def run(self) -> None:
        """Execute the realisation workflow."""
        self.runner.run()
