from __future__ import absolute_import
import datetime
from aniso8601 import parse_date, parse_datetime, parse_time
from graphql.error import GraphQLError
from graphql.language import StringValueNode, print_ast
from .scalars import Scalar


class Date(Scalar):
    """
    The `Date` scalar type represents a Date
    value as specified by
    [iso8601](https://en.wikipedia.org/wiki/ISO_8601).
    """


class DateTime(Scalar):
    """
    The `DateTime` scalar type represents a DateTime
    value as specified by
    [iso8601](https://en.wikipedia.org/wiki/ISO_8601).
    """


class Time(Scalar):
    """
    The `Time` scalar type represents a Time value as
    specified by
    [iso8601](https://en.wikipedia.org/wiki/ISO_8601).
    """
