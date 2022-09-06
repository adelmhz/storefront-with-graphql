import graphene
from graphql_jwt.decorators import login_required
from .types import UserType
from .mutations import CreateUser, EditUser, DeleteUser

class UserQuery(graphene.ObjectType):
    """Query to retrieve authenticated user."""
    me = graphene.Field(UserType)

    @login_required
    def resolve_me(root, info):
        return info.context.user

class UserMutation(graphene.ObjectType):
    """Mutation for create, update and delete user."""
    create_user = CreateUser.Field()
    edit_user = EditUser.Field()
    delete_user = DeleteUser.Field()