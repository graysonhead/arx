class ArxException(Exception):
    """
    Base class for arx Exceptions
    """

    def __init__(self, msg):
        self.msg = msg


class ArxExecutionException(ArxException):
    """
    Raised with an anomolous situation or error occurs during execution
    """
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return f"<ArxExecutionException: {self.msg}"


class ArxValidationError(ArxException):
    """
    Raised when an invalid configuration is present
    """
    def __init__(self, msg):
        self.msg = msg



class ArxNotConnectedError(ArxException):
    def __init__(self, msg):
        self.msg = msg


class ArxNotImplementedException(ArxException):
    """
    Raised when a module forgets to implement a required method
    """

    def __init(self, msg):
        self.msg = msg


class ArxConnectionError(ArxException):

    def __init__(self, msg=None):
        self.msg = msg

    def __str__(self):
        return f"<ArxConnectionException: {self.msg}>"