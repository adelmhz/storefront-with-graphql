import graphene
import graphql_jwt
from graphene_django.debug import DjangoDebug
from .store.schema import (CollectionQuery, ProductQuery, ReviewQuery,
                          CartQuery, CollectionMutation, ProductMutation,
                          PromotionQuery)
from .customer.schema import UserQuery


class Query(CollectionQuery, ProductQuery, ReviewQuery,
        PromotionQuery, CartQuery, UserQuery):
    debug = graphene.Field(DjangoDebug, name='_debug')


class Mutation(CollectionMutation, ProductMutation):
    token_auth = graphql_jwt.relay.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.relay.Verify.Field()
    refresh_token = graphql_jwt.relay.Refresh.Field()
    delete_token_cookie = graphql_jwt.relay.DeleteJSONWebTokenCookie.Field()

    # Long running refresh tokens
    revoke_token = graphql_jwt.relay.Revoke.Field()

    delete_refresh_token_cookie = \
        graphql_jwt.relay.DeleteRefreshTokenCookie.Field()



schema = graphene.Schema(query=Query,mutation=Mutation)
