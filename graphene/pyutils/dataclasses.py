import re
import sys
import copy
import types
import inspect
import keyword
__all__ = ['dataclass', 'field', 'Field', 'FrozenInstanceError', 'InitVar',
    'MISSING', 'fields', 'asdict', 'astuple', 'make_dataclass', 'replace',
    'is_dataclass']


class FrozenInstanceError(AttributeError):
    pass


class _HAS_DEFAULT_FACTORY_CLASS:

    def __repr__(self):
        return '<factory>'


_HAS_DEFAULT_FACTORY = _HAS_DEFAULT_FACTORY_CLASS()


class _MISSING_TYPE:
    pass


MISSING = _MISSING_TYPE()
_EMPTY_METADATA = types.MappingProxyType({})


class _FIELD_BASE:

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return self.name


_FIELD = _FIELD_BASE('_FIELD')
_FIELD_CLASSVAR = _FIELD_BASE('_FIELD_CLASSVAR')
_FIELD_INITVAR = _FIELD_BASE('_FIELD_INITVAR')
_FIELDS = '__dataclass_fields__'
_PARAMS = '__dataclass_params__'
_POST_INIT_NAME = '__post_init__'
_MODULE_IDENTIFIER_RE = re.compile('^(?:\\s*(\\w+)\\s*\\.)?\\s*(\\w+)')


class _InitVarMeta(type):

    def __getitem__(self, params):
        return self


class InitVar(metaclass=_InitVarMeta):
    pass


class Field:
    __slots__ = ('name', 'type', 'default', 'default_factory', 'repr',
        'hash', 'init', 'compare', 'metadata', '_field_type')

    def __init__(self, default, default_factory, init, repr, hash, compare,
        metadata):
        self.name = None
        self.type = None
        self.default = default
        self.default_factory = default_factory
        self.init = init
        self.repr = repr
        self.hash = hash
        self.compare = compare
        self.metadata = _EMPTY_METADATA if metadata is None or len(metadata
            ) == 0 else types.MappingProxyType(metadata)
        self._field_type = None

    def __repr__(self):
        return (
            f'Field(name={self.name!r},type={self.type!r},default={self.default!r},default_factory={self.default_factory!r},init={self.init!r},repr={self.repr!r},hash={self.hash!r},compare={self.compare!r},metadata={self.metadata!r},_field_type={self._field_type})'
            )

    def __set_name__(self, owner, name):
        func = getattr(type(self.default), '__set_name__', None)
        if func:
            func(self.default, owner, name)


class _DataclassParams:
    __slots__ = 'init', 'repr', 'eq', 'order', 'unsafe_hash', 'frozen'

    def __init__(self, init, repr, eq, order, unsafe_hash, frozen):
        self.init = init
        self.repr = repr
        self.eq = eq
        self.order = order
        self.unsafe_hash = unsafe_hash
        self.frozen = frozen

    def __repr__(self):
        return (
            f'_DataclassParams(init={self.init!r},repr={self.repr!r},eq={self.eq!r},order={self.order!r},unsafe_hash={self.unsafe_hash!r},frozen={self.frozen!r})'
            )


def field(*, default=MISSING, default_factory=MISSING, init=True, repr=True,
    hash=None, compare=True, metadata=None):
    """Return an object to identify dataclass fields.

    default is the default value of the field.  default_factory is a
    0-argument function called to initialize a field's value.  If init
    is True, the field will be a parameter to the class's __init__()
    function.  If repr is True, the field will be included in the
    object's repr().  If hash is True, the field will be included in
    the object's hash().  If compare is True, the field will be used
    in comparison functions.  metadata, if specified, must be a
    mapping which is stored but not otherwise examined by dataclass.

    It is an error to specify both default and default_factory.
    """
    pass


_hash_action = {(False, False, False, False): None, (False, False, False, 
    True): None, (False, False, True, False): None, (False, False, True, 
    True): None, (False, True, False, False): _hash_set_none, (False, True,
    False, True): None, (False, True, True, False): _hash_add, (False, True,
    True, True): None, (True, False, False, False): _hash_add, (True, False,
    False, True): _hash_exception, (True, False, True, False): _hash_add, (
    True, False, True, True): _hash_exception, (True, True, False, False):
    _hash_add, (True, True, False, True): _hash_exception, (True, True, 
    True, False): _hash_add, (True, True, True, True): _hash_exception}


def dataclass(_cls=None, *, init=True, repr=True, eq=True, order=False,
    unsafe_hash=False, frozen=False):
    """Returns the same class as was passed in, with dunder methods
    added based on the fields defined in the class.

    Examines PEP 526 __annotations__ to determine fields.

    If init is true, an __init__() method is added to the class. If
    repr is true, a __repr__() method is added. If order is true, rich
    comparison dunder methods are added. If unsafe_hash is true, a
    __hash__() method function is added. If frozen is true, fields may
    not be assigned to after instance creation.
    """
    pass


def fields(class_or_instance):
    """Return a tuple describing the fields of this dataclass.

    Accepts a dataclass or an instance of one. Tuple elements are of
    type Field.
    """
    pass


def _is_dataclass_instance(obj):
    """Returns True if obj is an instance of a dataclass."""
    pass


def is_dataclass(obj):
    """Returns True if obj is a dataclass or an instance of a
    dataclass."""
    pass


def asdict(obj, *, dict_factory=dict):
    """Return the fields of a dataclass instance as a new dictionary mapping
    field names to field values.

    Example usage:

      @dataclass
      class C:
          x: int
          y: int

      c = C(1, 2)
      assert asdict(c) == {'x': 1, 'y': 2}

    If given, 'dict_factory' will be used instead of built-in dict.
    The function applies recursively to field values that are
    dataclass instances. This will also look into built-in containers:
    tuples, lists, and dicts.
    """
    pass


def astuple(obj, *, tuple_factory=tuple):
    """Return the fields of a dataclass instance as a new tuple of field values.

    Example usage::

      @dataclass
      class C:
          x: int
          y: int

    c = C(1, 2)
    assert astuple(c) == (1, 2)

    If given, 'tuple_factory' will be used instead of built-in tuple.
    The function applies recursively to field values that are
    dataclass instances. This will also look into built-in containers:
    tuples, lists, and dicts.
    """
    pass


def make_dataclass(cls_name, fields, *, bases=(), namespace=None, init=True,
    repr=True, eq=True, order=False, unsafe_hash=False, frozen=False):
    """Return a new dynamically created dataclass.

    The dataclass name will be 'cls_name'.  'fields' is an iterable
    of either (name), (name, type) or (name, type, Field) objects. If type is
    omitted, use the string 'typing.Any'.  Field objects are created by
    the equivalent of calling 'field(name, type [, Field-info])'.

      C = make_dataclass('C', ['x', ('y', int), ('z', int, field(init=False))], bases=(Base,))

    is equivalent to:

      @dataclass
      class C(Base):
          x: 'typing.Any'
          y: int
          z: int = field(init=False)

    For the bases and namespace parameters, see the builtin type() function.

    The parameters init, repr, eq, order, unsafe_hash, and frozen are passed to
    dataclass().
    """
    pass


def replace(obj, **changes):
    """Return a new object replacing specified fields with new values.

    This is especially useful for frozen classes.  Example usage:

      @dataclass(frozen=True)
      class C:
          x: int
          y: int

      c = C(1, 2)
      c1 = replace(c, x=3)
      assert c1.x == 3 and c1.y == 2
    """
    pass
