class AgentException(Exception):
    """Exception raised for errors in the agent creation process.

    Attributes:
        message -- explanation of the error
    """
    def __init__(self, message="There was an error in the agent creation process"):
        self.message = message
        super().__init__(self.message)


class RoutineException(Exception):
    """Exception raised for errors in the routine.

    Attributes:
        message -- explanation of the error
    """
    def __init__(self, message="There was an error in the routine"):
        self.message = message
        super().__init__(self.message)


class SubroutineException(Exception):
    """Exception raised for errors in the subroutine.

    Attributes:
        message -- explanation of the error
    """
    def __init__(self, message="There was an error in the subroutine"):
        self.message = message
        super().__init__(self.message)

class APIException(Exception):
    """Exception raised for API Errors.

    Attributes:
        message -- explanation of the error
    """
    def __init__(self, message="We are done here."):
        self.message = message
        super().__init__(self.message)
