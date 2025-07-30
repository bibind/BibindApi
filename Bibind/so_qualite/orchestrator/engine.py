"""Engine that orchestrates the qualite step."""

from langgraph import Graph
from langgraph import Runner
from langgraph import Node


class QualiteEngine:
    """Simple wrapper around LangGraph Runner."""

    def __init__(self, graph: Graph) -> None:
        self.runner = Runner(graph)

    def run(self) -> None:
        """Execute the qualite workflow."""
        self.runner.run()
