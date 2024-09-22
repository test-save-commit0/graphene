import functools
import inspect
import warnings
string_types = type(b''), type('')


def deprecated(reason):
    """
    This is a decorator which can be used to mark functions
    as deprecated. It will result in a warning being emitted
    when the function is used.
    """
    pass
