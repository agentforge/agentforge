import threading
from typing import Dict, Any, List, Protocol, Optional, Callable
from agentforge.ai.routines.routine import Routine
from agentforge.utils import logger
from queue import Queue

class Node:
    def __init__(self, execute: Callable[[Dict[str, Any]], Dict[str, Any]], dependencies: List['Node']):
        self.execute = execute
        self.dependencies = dependencies
        self.finished = threading.Event()

    def run(self, context: Dict[str, Any], tasks: Dict[str, Routine]) -> Dict[str, Any]:
        for dependency in self.dependencies:
            dependency.finished.wait()  # Wait until the dependency has finished

        logger.info(f"Running Node: {self.execute.__name__}")
        context = self.execute(context)

        self.finished.set()  # Signal that this node has finished
        return context

    def reset(self):
        self.finished.clear()  # Reset the finished event

class StateMachine:
    def __init__(self, nodes: List[Node], tasks: Dict[str, Routine]):
        self.nodes = nodes
        self.tasks = tasks

    def run(self, context: Dict[str, Any]) -> Dict[str, Any]:
        for node in self.nodes:
            try:
                threading.Thread(target=node.run, args=(context, self.tasks)).start()
            except Exception as e:
                logger.info(f"Error starting thread: {str(e)}")

        for node in self.nodes:
            node.finished.wait()  # Wait until the node has finished
        self.reset()  # Reset the nodes when all have finished
        return context

    def reset(self):
        for node in self.nodes:
            node.reset()  # Reset each node
