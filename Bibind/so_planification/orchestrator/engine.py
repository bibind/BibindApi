"""Engine that orchestrates the planification step."""

from langgraph import Graph
from langgraph import Runner
from langgraph import Node


class PlanificationEngine:
    """Simple wrapper around LangGraph Runner."""

    def __init__(self, graph: Graph) -> None:
        self.runner = Runner(graph)

    def run(self) -> None:
        """Execute the planification workflow."""
        self.runner.run()
