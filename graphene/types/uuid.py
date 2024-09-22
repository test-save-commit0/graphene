from __future__ import absolute_import
from uuid import UUID as _UUID
from graphql.language.ast import StringValueNode
from graphql import Undefined
from .scalars import Scalar


class UUID(Scalar):
    """
    Leverages the internal Python implementation of UUID (uuid.UUID) to provide native UUID objects
    in fields, resolvers and input.
    """
