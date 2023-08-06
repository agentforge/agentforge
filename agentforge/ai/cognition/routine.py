import json
from agentforge.ai import Subroutine
from typing import Dict, Any, Protocol, List, Optional
from agentforge.exceptions import SubroutineException
from agentforge.interfaces import interface_interactor
import traceback

### Describes a routine, i.e. going to the grocery store or reacting to user input
### A routine is a collection of subroutines with a specific order

## A Routine can be hijacked and run by another function
class Routine():
    def __init__(self, name: str, description: str = "") -> None:
        self.subroutines = []

        self.name = name if name is not None else ""
        self.phrases = description

        self.vectorstore = interface_interactor.get_interface("vectorstore")
        if description != "" and name != "":
            self.register_in_vectorstore()
    
    # Register this routine in a vectorstore so we can do similarity lookups
    # based on the attributes that describe it
    def register_in_vectorstore(self) -> None:
        try:
            # Check if the task_ exists in the vectorstore with metadata "task_: true"
            results = self.vectorstore.search(self.name, 1, filter={"task_": True}, collection="tasks")
            if not results:
                # If it does not exist, add it to the vectorstore with metadata "task_: true"
                self.vectorstore.add_texts(
                    self.phrases,
                    [{"task_": True, "task_name": self.name} for i in self.phrases],
                    collection="tasks"
                )
        except Exception as e:
            print(f"Error registering task_, tasks: List in vectorstore: {str(e)}")
            traceback.print_exc()
  
    # Run routine, each iteration of cognitive stack check to see if we need to divert the task_
    def run(self, context: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        for subroutine in self.subroutines:
            print(subroutine)
            context = subroutine.execute(context)
        return context
