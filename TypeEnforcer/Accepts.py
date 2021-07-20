#!/usr/bin/env python3.9

from TypeEnforcer.Exceptions import InvalidTypeError, MismatchedTypeError, NonUnionizedTypeError
import typing
from TypeEnforcer.HomogenousType import check_container


def has_union(parameter_types: list) -> bool:
    return any([isinstance(element, tuple) for element in parameter_types])


def check_in_union(parameterized_types: list, types: list) -> bool:
    """
    Ensure type is in unionized type for `accepts` decorator.
    Example [valid]:

    @accepts((float, int))
    def func(a: int):
        return a + a

    Example [invalid]:
    @accepts((float, int))
    def func(a: str):
        return a+=" hello"
    """
    _ret = False
    for x, (_param, _type) in enumerate(zip(parameterized_types, types)):
        if(isinstance(_param, tuple)):
            if not(_type in param):
                raise NonUnionizedTypeError(
                    f'argument {x} in function parameters is type {_type} which is not present in union {_param}')
            _ret = True
    return _ret


def preliminary_type_check(function: typing.Callable, types: tuple) -> tuple[list, bool]:
    """
    Ensure parameter types from function declaration and
    types given to `accepts` decorator match up
    """

    params = function.__code__.co_varnames
    parameter_types = list(function.__annotations__.values())
    _len_params, _len_types = len(params), len(types)

    if(_len_params != _len_types):
        raise ValueError(
            f'number of parameters({_len_params}) does not match number of types ({_len_types})')
    has_unionization = check_in_union(parameter_types, types)
    print(parameter_types, types)
    if(parameter_types != types):
        # for(param,  _type) in zip(parameter_types, types):
        # if(not check_in_union(param, types) or
        # (param != _type)):
        raise MismatchedTypeError(
            f'types given in accepts{types} does not match function declaration: {function.__name__}({parameter_types})')

    _is_class = False if not("self" in params) else True
    return (parameter_types, _is_class)


def is_generic(_type) -> bool:
    return hasattr(_type, '__origin__')


def is_nested_generic(_type) -> bool:
    if(is_generic(_type)):
        if(any([hasattr(element, '__args__') for element in _type.__args__])):
            raise NestedGenericError(
                f'nested generics are currently unsupported')
    return False


def accepts(*types):
    """
    A series of types that can be accepted in the
    function declaration
    """

    def check_types_accepted(__original_function: typing.Callable):
        args, _is_class = preliminary_type_check(__original_function, types)

        def new_function(*args, **kwds):
            save_state = args  # restore function parameters for class declarations
            if(_is_class):
                args = args[1:]
            for (argument, _type) in zip(args, types):
                # will raise NestedGenericError
                _generic = is_generic(_type)
                status = is_nested_generic(_type)

                if(_generic):
                    _returned_type, status, index = check_container(
                        argument, _type.__args__[0])
                    if not(status):
                        raise MismatchedTypeError(
                            f'container ({_type.__origin__.__name__}) declared to house type ({_type.__args__[0].__name__})')
                else:
                    if not(isinstance(argument, _type)):
                        message = f'arg ({argument} => {type(argument).__name__}) does not match type(s) {_type}'
                        raise InvalidTypeError(message)
            args = save_state
            return __original_function(*args, **kwds)
        new_function.__name__ = __original_function.__name__
        return new_function
    return check_types_accepted
