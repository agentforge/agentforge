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

    def run(self, context: Dict[str, Any], flows: Dict[str, Routine]) -> Dict[str, Any]:
        for dependency in self.dependencies:
            dependency.finished.wait()  # Wait until the dependency has finished
        try:
            new_context = self.execute(context)
            context.update(new_context)
        except BreakRoutineException as interruption:
            routine = flows[str(interruption)]
            new_context = StateMachine(routine.subroutines, flows).run(context)
            context.update(new_context)
        self.finished.set()  # Signal that this node has finished
        return context

class StateMachine:
    def __init__(self, nodes: List[Node], flows: Dict[str, Routine]):
        self.nodes = nodes
        self.flows = flows

    def run(self, context: Dict[str, Any]) -> Dict[str, Any]:
        for node in self.nodes:
            threading.Thread(target=node.run, args=(context, self.flows)).start()
        for node in self.nodes:
            node.finished.wait()  # Wait until the node has finished
        return context
