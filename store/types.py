from graphene import relay
from graphene_django import DjangoObjectType
from .models import Product, Collection, Review, Cart, Promotion
from django.contrib.auth import get_user_model

class UserType(DjangoObjectType):
    class Meta:
        exclude = ('password',)
        interfaces = (relay.Node, )
        model = get_user_model()

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

class PromotionType(DjangoObjectType):
    class Meta:
        model = Promotion
        fields = '__all__'
        interfaces = (relay.Node, )

class ReviewType(DjangoObjectType):
    class Meta:
        model = Review
        fields = '__all__'
        interfaces = (relay.Node, )

    @classmethod
    def get_queryset(cls, queryset, info):
        return queryset.select_related('product')

class CartType(DjangoObjectType):
    class Meta:
        model = Cart
        fields = '__all__'
        interfaces = (relay.Node, )