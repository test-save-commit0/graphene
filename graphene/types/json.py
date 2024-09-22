from __future__ import absolute_import
import json
from graphql import Undefined
from graphql.language.ast import StringValueNode
from .scalars import Scalar


class JSONString(Scalar):
    """
    Allows use of a JSON String for input / output from the GraphQL schema.

    Use of this type is *not recommended* as you lose the benefits of having a defined, static
    schema (one of the key benefits of GraphQL).
    """
