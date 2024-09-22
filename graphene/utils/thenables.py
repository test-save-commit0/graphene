"""
This file is used mainly as a bridge for thenable abstractions.
"""
from inspect import isawaitable


def maybe_thenable(obj, on_resolve):
    """
    Execute a on_resolve function once the thenable is resolved,
    returning the same type of object inputed.
    If the object is not thenable, it should return on_resolve(obj)
    """
    pass
