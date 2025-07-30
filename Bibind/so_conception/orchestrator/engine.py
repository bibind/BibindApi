"""Engine that orchestrates the conception step."""

from langgraph import Graph
from langgraph import Runner
from langgraph import Node


class ConceptionEngine:
    """Simple wrapper around LangGraph Runner."""

    def __init__(self, graph: Graph) -> None:
        self.runner = Runner(graph)

    def run(self) -> None:
        """Execute the conception workflow."""
        self.runner.run()
