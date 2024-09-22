from graphql import GraphQLError
from graphql.language import FieldNode
from graphql.validation import ValidationRule
from ..utils.is_introspection_key import is_introspection_key


class DisableIntrospection(ValidationRule):
    pass
