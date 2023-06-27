class DecisionException(Exception):
    """Exception raised for errors in the decision making process.

    Attributes:
        message -- explanation of the error
    """
    def __init__(self, message="There was an error in the decision making process"):
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

class BreakRoutineException(Exception):
    """Exception raised for breaking out of a routine.

    Attributes:
        message -- explanation of the error
    """
    def __init__(self, message="We are done here."):
        self.message = message
        super().__init__(self.message)
