from typing import Any
from graphql import Undefined
from graphql.language.ast import BooleanValueNode, FloatValueNode, IntValueNode, StringValueNode
from .base import BaseOptions, BaseType
from .unmountedtype import UnmountedType


class ScalarOptions(BaseOptions):
    pass


class Scalar(UnmountedType, BaseType):
    """
    Scalar Type Definition

    The leaf values of any request and input values to arguments are
    Scalars (or Enums) and are defined with a name and a series of functions
    used to parse input from ast or variables and to ensure validity.
    """

    @classmethod
    def __init_subclass_with_meta__(cls, **options):
        _meta = ScalarOptions(cls)
        super(Scalar, cls).__init_subclass_with_meta__(_meta=_meta, **options)
    serialize = None
    parse_value = None
    parse_literal = None

    @classmethod
    def get_type(cls):
        """
        This function is called when the unmounted type (Scalar instance)
        is mounted (as a Field, InputField or Argument)
        """
        from graphql import GraphQLScalarType

        return GraphQLScalarType(
            name=cls._meta.name,
            description=cls._meta.description,
            serialize=cls.serialize,
            parse_value=cls.parse_value,
            parse_literal=cls.parse_literal,
        )


MAX_INT = 2147483647
MIN_INT = -2147483648


def coerce_int(value):
    if isinstance(value, bool):
        return 1 if value else 0
    try:
        int_value = int(value)
        if MIN_INT <= int_value <= MAX_INT:
            return int_value
    except (TypeError, ValueError):
        pass
    raise ValueError(f"Int cannot represent non 32-bit signed integer value: {value}")

class Int(Scalar):
    """
    The `Int` scalar type represents non-fractional signed whole numeric
    values. Int can represent values between -(2^31) and 2^31 - 1 since
    represented in JSON as double-precision floating point numbers specified
    by [IEEE 754](http://en.wikipedia.org/wiki/IEEE_floating_point).
    """
    serialize = coerce_int
    parse_value = coerce_int

    @classmethod
    def parse_literal(cls, node):
        if isinstance(node, IntValueNode):
            return coerce_int(node.value)


def coerce_big_int(value):
    try:
        return int(value)
    except (TypeError, ValueError):
        raise ValueError(f"BigInt cannot represent non-integer value: {value}")

class BigInt(Scalar):
    """
    The `BigInt` scalar type represents non-fractional whole numeric values.
    `BigInt` is not constrained to 32-bit like the `Int` type and thus is a less
    compatible type.
    """
    serialize = coerce_big_int
    parse_value = coerce_big_int

    @classmethod
    def parse_literal(cls, node):
        if isinstance(node, IntValueNode):
            return coerce_big_int(node.value)

def coerce_float(value):
    try:
        return float(value)
    except (TypeError, ValueError):
        raise ValueError(f"Float cannot represent non numeric value: {value}")

class Float(Scalar):
    """
    The `Float` scalar type represents signed double-precision fractional
    values as specified by
    [IEEE 754](http://en.wikipedia.org/wiki/IEEE_floating_point).
    """
    serialize = coerce_float
    parse_value = coerce_float

    @classmethod
    def parse_literal(cls, node):
        if isinstance(node, (FloatValueNode, IntValueNode)):
            return coerce_float(node.value)

def coerce_string(value):
    if isinstance(value, str):
        return value
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, int) or isinstance(value, float):
        return str(value)
    if isinstance(value, dict) or isinstance(value, list):
        raise ValueError(f"String cannot represent value: {value}")
    return str(value)

class String(Scalar):
    """
    The `String` scalar type represents textual data, represented as UTF-8
    character sequences. The String type is most often used by GraphQL to
    represent free-form human-readable text.
    """
    serialize = coerce_string
    parse_value = coerce_string

    @classmethod
    def parse_literal(cls, node):
        if isinstance(node, StringValueNode):
            return node.value


class Boolean(Scalar):
    """
    The `Boolean` scalar type represents `true` or `false`.
    """
    serialize = bool
    parse_value = bool

    @classmethod
    def parse_literal(cls, node):
        if isinstance(node, BooleanValueNode):
            return node.value

class ID(Scalar):
    """
    The `ID` scalar type represents a unique identifier, often used to
    refetch an object or as key for a cache. The ID type appears in a JSON
    response as a String; however, it is not intended to be human-readable.
    When expected as an input type, any string (such as `"4"`) or integer
    (such as `4`) input value will be accepted as an ID.
    """
    serialize = str
    parse_value = str

    @classmethod
    def parse_literal(cls, node):
        if isinstance(node, (StringValueNode, IntValueNode)):
            return node.value
