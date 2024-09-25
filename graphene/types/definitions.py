from enum import Enum as PyEnum
from graphql import GraphQLEnumType, GraphQLInputObjectType, GraphQLInterfaceType, GraphQLObjectType, GraphQLScalarType, GraphQLUnionType


class GrapheneGraphQLType:
    """
    A class for extending the base GraphQLType with the related
    graphene_type
    """

    def __init__(self, *args, **kwargs):
        self.graphene_type = kwargs.pop('graphene_type')
        super(GrapheneGraphQLType, self).__init__(*args, **kwargs)

    def __copy__(self):
        result = GrapheneGraphQLType(graphene_type=self.graphene_type)
        result.__dict__.update(self.__dict__)
        return result


class GrapheneInterfaceType(GrapheneGraphQLType, GraphQLInterfaceType):
    def __copy__(self):
        result = GrapheneInterfaceType(graphene_type=self.graphene_type)
        result.__dict__.update(self.__dict__)
        return result


class GrapheneUnionType(GrapheneGraphQLType, GraphQLUnionType):
    def __copy__(self):
        result = GrapheneUnionType(graphene_type=self.graphene_type)
        result.__dict__.update(self.__dict__)
        return result


class GrapheneObjectType(GrapheneGraphQLType, GraphQLObjectType):
    def __copy__(self):
        result = GrapheneObjectType(graphene_type=self.graphene_type)
        result.__dict__.update(self.__dict__)
        return result


class GrapheneScalarType(GrapheneGraphQLType, GraphQLScalarType):
    def __copy__(self):
        result = GrapheneScalarType(graphene_type=self.graphene_type)
        result.__dict__.update(self.__dict__)
        return result


class GrapheneEnumType(GrapheneGraphQLType, GraphQLEnumType):
    def __copy__(self):
        result = GrapheneEnumType(graphene_type=self.graphene_type)
        result.__dict__.update(self.__dict__)
        return result


class GrapheneInputObjectType(GrapheneGraphQLType, GraphQLInputObjectType):
    def __copy__(self):
        result = GrapheneInputObjectType(graphene_type=self.graphene_type)
        result.__dict__.update(self.__dict__)
        return result
