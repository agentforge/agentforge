from typing import Dict, Any, Protocol, Optional

### A subroutine is a single atomic action that can be executed by the agent
### Context comes from the previous subroutine and is passed to the next subroutine
class Subroutine(Protocol):
    def execute(self, context: Optional[Dict[str, Any]]) -> Dict[str, Any]: ...