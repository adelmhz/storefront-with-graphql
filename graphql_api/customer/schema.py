import graphene
from graphql_jwt.decorators import login_required
from .types import UserType


class UserQuery(graphene.ObjectType):
    """Query to retrieve authenticated user."""
    me = graphene.Field(UserType)

    @login_required
    def resolve_me(root, info):
        return info.context.user