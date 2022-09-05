from graphene import relay
from graphene_django import DjangoObjectType
from django.contrib.auth import get_user_model

class UserType(DjangoObjectType):
    class Meta:
        exclude = ('password',)
        interfaces = (relay.Node, )
        model = get_user_model()