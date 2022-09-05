from graphene import relay
from graphene_django import DjangoObjectType
from .models import Product, Collection, Review, Cart, Promotion
from django.contrib.auth import get_user_model


class CollectionType(DjangoObjectType):
    class Meta:
        fields = ('id', 'title', 'products', 'featured_product')
        filter_fields = {
            'title': ['exact', 'icontains', 'istartswith'],
            'id': ['exact']
        }
        interfaces = (relay.Node, )
        model = Collection

    @classmethod
    def get_queryset(cls, queryset, info):
        return queryset.prefetch_related('products')


class ProductType(DjangoObjectType):
    class Meta:
        model = Product
        interfaces = (relay.Node, )

    @classmethod
    def get_queryset(cls, queryset, info):
        return queryset.select_related('collection')
