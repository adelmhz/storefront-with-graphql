import graphene
import graphql_jwt
from graphene_django.debug import DjangoDebug
from store.schema import CollectionQuery, CollectionMutation,


class Query(CollectionQuery):
    debug = graphene.Field(DjangoDebug, name='_debug')


class Mutation(CollectionMutation):
    pass



schema = graphene.Schema(query=Query,mutation=Mutation)
