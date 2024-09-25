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
    def decorator(func):
        if isinstance(func, type):
            fmt = "Call to deprecated class {name} ({reason})."
        else:
            fmt = "Call to deprecated function {name} ({reason})."

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            warnings.warn(
                fmt.format(name=func.__name__, reason=reason),
                category=DeprecationWarning,
                stacklevel=2
            )
            return func(*args, **kwargs)

        return wrapper

    if isinstance(reason, string_types):
        return decorator
    else:
        return decorator(reason)
