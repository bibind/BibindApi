"""Engine that orchestrates the release step."""

from langgraph import Graph
from langgraph import Runner
from langgraph import Node


class ReleaseEngine:
    """Simple wrapper around LangGraph Runner."""

    def __init__(self, graph: Graph) -> None:
        self.runner = Runner(graph)

    def run(self) -> None:
        """Execute the release workflow."""
        self.runner.run()
