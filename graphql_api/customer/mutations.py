import graphene
from graphql import GraphQLError
from graphql_jwt.decorators import staff_member_required, superuser_required
from django.db import transaction
from customer.models import Customer
from core.models import User
from .types import UserType

class CreateUser(graphene.Mutation):
    """Mutation for creating user."""
    class Arguments:
        username = graphene.String(required=True)
        email = graphene.String(required=True)
        password = graphene.String(required=True)
        first_name = graphene.String()
        last_name = graphene.String()
        is_staff = graphene.Boolean()
        is_active = graphene.Boolean()
        date_joined = graphene.DateTime()

    user = graphene.Field(UserType)

    @classmethod
    @superuser_required
    def mutate(
    cls, root, info, **extra_fields):
        user = User.objects.create_user(**extra_fields)


        return CreateUser(user=user)

class EditUser(graphene.Mutation):
    """Mutation for updating user."""
    class Arguments:
        username = graphene.String(required=True)
        email = graphene.String()
        password = graphene.String()
        first_name = graphene.String()
        last_name = graphene.String()
        is_staff = graphene.Boolean()
        is_active = graphene.Boolean()
        date_joined = graphene.DateTime()

    user = graphene.Field(UserType)

    @classmethod
    @superuser_required
    def mutate(
    cls, root, info, **extra_fields):
        username = extra_fields.pop('username', None)
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise GraphQLError("User dose not exist.")
        email = extra_fields.pop('email', None)
        password = extra_fields.pop('password', None)

        for attr, value in extra_fields.items():
                setattr(user, attr, value)
        if email:
            user.email = User.objects.normalize_email(email)
        if password:
            user.set_password(password)



        return CreateUser(user=user)

class DeleteUser(graphene.Mutation):
    class Arguments:
        username = graphene.String(required=True)

    ok = graphene.Boolean()

    @classmethod
    @superuser_required
    def mutate(cls, root, info, username):
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise GraphQLError("User dose not exist.")
        user.delete()

        return DeleteUser(ok=True)
