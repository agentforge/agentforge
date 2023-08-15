import threading
from typing import Dict, Any, List, Protocol, Optional, Callable
from agentforge.ai.routines.routine import Routine
from agentforge.exceptions import BreakRoutineException

from queue import Queue

class Node:
    def __init__(self, execute: Callable[[Dict[str, Any]], Dict[str, Any]], dependencies: List['Node']):
        self.execute = execute
        self.dependencies = dependencies
        self.finished = threading.Event()

    def run(self, context: Dict[str, Any], tasks: Dict[str, Routine]) -> Dict[str, Any]:
        for dependency in self.dependencies:
            dependency.finished.wait()  # Wait until the dependency has finished
            print(dependency, " finished..")
        try:
            print("EXECUTING NODE", self.execute)
            context = self.execute(context)
        except BreakRoutineException as interruption:
            routine = tasks[str(interruption)]
            context = StateMachine(routine.subroutines, tasks).run(context)
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
            threading.Thread(target=node.run, args=(context, self.tasks)).start()
        for node in self.nodes:
            node.finished.wait()  # Wait until the node has finished
        self.reset()  # Reset the nodes when all have finished
        return context

    def reset(self):
        for node in self.nodes:
            node.reset()  # Reset each node
