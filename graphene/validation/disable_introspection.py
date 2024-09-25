from graphql import GraphQLError
from graphql.language import FieldNode
from graphql.validation import ValidationRule
from ..utils.is_introspection_key import is_introspection_key


class DisableIntrospection(ValidationRule):
    def enter_field(self, node: FieldNode, *args):
        if is_introspection_key(node.name.value):
            raise GraphQLError(
                f"GraphQL introspection is not allowed, but the query contained {node.name.value}",
                [node]
            )
