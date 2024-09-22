from graphql_relay import from_global_id, to_global_id
from ..types import ID, UUID
from ..types.base import BaseType
from typing import Type


class BaseGlobalIDType:
    """
    Base class that define the required attributes/method for a type.
    """
    graphene_type = ID


class DefaultGlobalIDType(BaseGlobalIDType):
    """
    Default global ID type: base64 encoded version of "<node type name>: <node id>".
    """
    graphene_type = ID


class SimpleGlobalIDType(BaseGlobalIDType):
    """
    Simple global ID type: simply the id of the object.
    To be used carefully as the user is responsible for ensuring that the IDs are indeed global
    (otherwise it could cause request caching issues).
    """
    graphene_type = ID


class UUIDGlobalIDType(BaseGlobalIDType):
    """
    UUID global ID type.
    By definition UUID are global so they are used as they are.
    """
    graphene_type = UUID
