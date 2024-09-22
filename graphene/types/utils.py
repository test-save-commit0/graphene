import inspect
from functools import partial
from ..utils.module_loading import import_string
from .mountedtype import MountedType
from .unmountedtype import UnmountedType


def get_field_as(value, _as=None):
    """
    Get type mounted
    """
    pass


def yank_fields_from_attrs(attrs, _as=None, sort=True):
    """
    Extract all the fields in given attributes (dict)
    and return them ordered
    """
    pass


def get_underlying_type(_type):
    """Get the underlying type even if it is wrapped in structures like NonNull"""
    pass
