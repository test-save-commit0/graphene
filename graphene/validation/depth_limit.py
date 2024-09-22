try:
    from re import Pattern
except ImportError:
    from typing import Pattern
from typing import Callable, Dict, List, Optional, Union, Tuple
from graphql import GraphQLError
from graphql.validation import ValidationContext, ValidationRule
from graphql.language import DefinitionNode, FieldNode, FragmentDefinitionNode, FragmentSpreadNode, InlineFragmentNode, Node, OperationDefinitionNode
from ..utils.is_introspection_key import is_introspection_key
IgnoreType = Union[Callable[[str], bool], Pattern, str]
