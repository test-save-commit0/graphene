class _OldClass:
    pass


class _NewClass:
    pass


_all_vars = set(dir(_OldClass) + dir(_NewClass))


def props(x):
    """
    Return a list of all properties (including methods) of the given object,
    excluding those that are present in both _OldClass and _NewClass.
    """
    return [prop for prop in dir(x) if prop not in _all_vars]


def get_props(x):
    """
    Return a dictionary of all properties (including methods) of the given object,
    excluding those that are present in both _OldClass and _NewClass.
    The keys are the property names, and the values are the property values.
    """
    return {prop: getattr(x, prop) for prop in props(x)}
