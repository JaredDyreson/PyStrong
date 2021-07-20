class PyStrongBaseException(Exception):
    def __init__(self, message: str):
        if not(isinstance(message, str)):
            raise ValueError(
                f'expected `str`; obtained {type(message).__name__}')
        self.message = message


class InvalidTypeError(PyStrongBaseException):
    """
    Can be seen as child to below exception
    If iterating over container holding types from function declaration and
    types do not line up, this exception is thrown
    """

    def __init__(self, message: str):
        super().__init__(message)


class MismatchedTypeError(PyStrongBaseException):
    """
    a = [int, int, int]
    =>
    b = [int, float, int]

    Exception thrown because of index 1
    Used when two containers are compared
    """

    def __init__(self, message: str):
        super().__init__(message)


class NonUnionizedTypeError(PyStrongBaseException):
    """
    Exception thrown when type is not apart of union:

    allowed_types: (float, int)
    given_type: str

    given_type not in allowed_types
    """

    def __init__(self, message: str):
        super().__init__(message)


class NestedGenericError(PyStrongBaseException):
    """
    Exception thrown when encountering nested generic:
    list[list[str]] <- exception
    list[str] <- no exception
    """

    def __init__(self, message: str):
        super().__init__(message)
