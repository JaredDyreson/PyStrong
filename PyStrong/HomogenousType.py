#!/usr/bin/env python3.9

def check_container(container, _type) -> tuple:
    """
    Given a container object, check and see if the contents match
    the specified type

    If the test fails, return the offending type, false flag and the offending index
    """
    if not(hasattr(container, '__iter__')):
        raise ValueError(
            f'expecting container object, received: {type(container).__name__}')
    for i, element in enumerate(container):
        if not(isinstance(element, _type)):
            return (type(element), False, i)
    return (_type, True, -1)
