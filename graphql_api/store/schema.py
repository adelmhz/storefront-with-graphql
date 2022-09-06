import graphene
from graphql import GraphQLError
from graphene_django.filter import DjangoFilterConnectionField
from graphql_jwt.decorators import staff_member_required, login_required
from django.db import transaction
from store.models import Product, Collection, Review, Cart, Promotion
from .filters import ProductFilter, ReviewFilter, PromotionFilter
from .types import (CollectionType, ProductType, ReviewType,
                    CartType, PromotionType)
from .mutations import (
    CreateCollection, EditCollection, DeleteCollection,
    CreateProduct, EditProduct, DeleteProduct,
    DeleteProductPromotions, CreatePromotion, EditPromotion,
    DeletePromotion,
    )

class CollectionQuery(graphene.ObjectType):
    """Query to retrieve collections."""
    collections = DjangoFilterConnectionField(CollectionType)

class CollectionMutation(graphene.ObjectType):
    """Mutation class for create, update and delete a collection"""
    create_collection = CreateCollection.Field()
    edit_collection = EditCollection.Field()
    delete_collection = DeleteCollection.Field()


class ProductQuery(graphene.ObjectType):
    """Query for get all products or retrieve a product."""
    all_products = DjangoFilterConnectionField(
        ProductType, filterset_class=ProductFilter)
    product = graphene.Field(
        ProductType, product_id=graphene.ID(required=True))

    def resolve_product(root, info, product_id):
        try:
            return Product.objects.get(pk=product_id)
        except Product.DoesNotExist:
            raise GraphQLError(message="Product does not exist.")

class ProductMutation(graphene.ObjectType):
    """Mutating class for create, update, delete and promotions of product."""
    create_product = CreateProduct.Field()
    edit_product = EditProduct.Field()
    delete_product_promotions = DeleteProductPromotions.Field()
    delete_product = DeleteProduct.Field()


class PromotionQuery(graphene.ObjectType):
    """Query for retrieve promotions."""
    promotion = graphene.Field(
        PromotionType, promotion_id=graphene.ID(required=True))
    all_promotions = DjangoFilterConnectionField(
        PromotionType, filterset_class=PromotionFilter
    )

    @staff_member_required
    def resolve_promotion(root, info, promotion_id):
        try:
            return Promotion.objects.get(pk=promotion_id)
        except Promotion.DoesNotExist:
            raise GraphQLError(message='Promotion dose not exist.')

class PromotionMutation(graphene.ObjectType):
    """Mutating class for create, update and delete promotion."""

    create_promotion = CreatePromotion.Field()
    edit_promotion = EditPromotion.Field()
    delete_promotion = DeletePromotion.Field()

class ReviewQuery(graphene.ObjectType):
    """Query for retrieve review or reviews of product"""
    reviews_of_product = DjangoFilterConnectionField(
        ReviewType, filterset_class=ReviewFilter, product_id=graphene.ID(required=True))
    review = graphene.Field(ReviewType, review_id=graphene.ID(required=True))

    def resolve_reviews_of_product(root, info, product_id):
        return Review.objects.filter(product_id=product_id)

    def resolve_review(root, info, review_id):
        try:
            return Review.objects.get(pk=review_id)
        except Review.DoesNotExist:
            raise GraphQLError(message='Review dose not exist.')


class CartQuery(graphene.ObjectType):
    """Query for retrieve a cart."""
    cart = graphene.Field(CartType, cart_id=graphene.ID(required=True))

    @login_required
    def resolve_cart(root, info, cart_id):
        return Cart.objects.get(pk=cart_id)
