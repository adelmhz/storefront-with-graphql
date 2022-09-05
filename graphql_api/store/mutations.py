import graphene
from graphql import GraphQLError
from graphql_jwt.decorators import staff_member_required
from django.db import transaction
from store.models import Product, Collection, Promotion
from .types import CollectionType, ProductType


class CreateCollection(graphene.Mutation):
    """Mutation for creating a collection."""
    class Arguments:
        title = graphene.String(required=True)
        featured_product_id = graphene.ID()

    collection = graphene.Field(CollectionType)

    @classmethod
    @staff_member_required
    def mutate(cls, root, info, title, featured_product_id=None):
        collection = Collection()
        collection.title = title
        if featured_product_id:
            try:
                featured_product = Product.objects.get(pk=featured_product_id)
                collection.featured_product = featured_product
            except Product.DoesNotExist:
                raise GraphQLError('Featured product dose not exist.')
        collection.save()

        return CreateCollection(collection=collection)


class EditCollection(graphene.Mutation):
    """Mutation for updating a collection."""
    class Arguments:
        collection_id = graphene.ID(required=True)
        title = graphene.String(required=True)
        featured_product_id = graphene.ID()

    collection = graphene.Field(CollectionType)

    @classmethod
    @staff_member_required
    def mutate(cls, root, info, title, collection_id, featured_product_id=None):
        try:
            collection = Collection.objects.get(pk=collection_id)
        except Collection.DoesNotExist:
            raise GraphQLError('Collection dose not exist.')
        collection.title = title
        if featured_product_id:
            try:
                featured_product = Product.objects.get(pk=featured_product_id)
            except Product.DoesNotExist:
                raise GraphQLError('Product dose not exist.')
            collection.featured_product = featured_product
        collection.save()

        return CreateCollection(collection=collection)


class DeleteCollection(graphene.Mutation):
    """Mutation for deleting a collection."""
    class Arguments:
        collection_id = graphene.ID(required=True)

    ok = graphene.Boolean()

    @classmethod
    @staff_member_required
    def mutate(cls, root, info, collection_id):
        try:
            collection = Collection.objects.get(pk=collection_id)
            collection.delete()
        except Collection.DoesNotExist:
            raise GraphQLError('Collection dose not exist.')

        return DeleteCollection(ok=True)


class CreateProduct(graphene.Mutation):
    """Mutation for creating a product."""
    class Arguments:
        title = graphene.String(required=True)
        slug = graphene.String(required=True)
        description = graphene.String()
        unit_price = graphene.Decimal(required=True)
        inventory = graphene.Int(required=True)
        collection_id = graphene.ID(required=True)
        promotions = graphene.List(graphene.Int)

    product = graphene.Field(ProductType)

    @classmethod
    @staff_member_required
    def mutate(cls, root, info, **kwargs):
        with transaction.atomic():
            collection_id = kwargs.pop('collection_id', None)
            promotions = kwargs.pop('promotions', None)

            product = Product()
            for attr, value in kwargs.items():
                setattr(product, attr, value)

            product.save()

            try:
                collection = Collection.objects.get(pk=collection_id)
                product.collection = collection
            except Collection.DoesNotExist:
                raise GraphQLError('Collection dose not exist.')

            if promotions:
                for promotion_id in promotions:
                    try:
                        promotion = Promotion.objects.get(pk=promotion_id)
                        product.promotions.add(promotion)
                    except Promotion.DoesNotExist:
                        raise GraphQLError('Promotion dose not exist.')

            return CreateProduct(product=product)


class EditProduct(graphene.Mutation):
    """Mutation for updating a product."""
    class Arguments:
        product_id = graphene.ID(required=True)
        title = graphene.String()
        slug = graphene.String()
        description = graphene.String()
        unit_price = graphene.Decimal()
        inventory = graphene.Int()
        collection_id = graphene.ID()
        promotions = graphene.List(graphene.Int)

    product = graphene.Field(ProductType)

    @classmethod
    @staff_member_required
    def mutate(cls, root, info, **kwargs):
        product_id = kwargs.pop('product_id', None)
        collection_id = kwargs.pop('collection_id', None)
        promotions = kwargs.pop('promotions', None)

        with transaction.atomic():
            try:
                product = Product.objects.get(pk=product_id)
            except Product.DoesNotExist:
                raise GraphQLError("Product does not exist.")

            for attr, value in kwargs.items():
                setattr(product, attr, value)

            if collection_id:
                try:
                    collection = Collection.objects.get(pk=collection_id)
                    product.collection = collection
                except Collection.DoesNotExist:
                    raise GraphQLError("collection does not exist.")

            if promotions:
                for promotion_id in promotions:
                    try:
                        promotion = Promotion.objects.get(pk=promotion_id)
                        product.promotions.add(promotion)
                    except Promotion.DoesNotExist:
                        raise GraphQLError('Promotion dose not exist.')

        return CreateProduct(product=product)


class DeleteProductPromotions(graphene.Mutation):
    """Mutation for deleting promotions of a product."""
    class Arguments:
        product_id = graphene.ID(required=True)

    ok = graphene.String()

    @classmethod
    @staff_member_required
    def mutate(cls, root, info, product_id):
        try:
            product = Product.objects.get(pk=product_id)
            product.promotions.clear()
            return DeleteProductPromotions(ok="ok")
        except Product.DoesNotExist:
            raise GraphQLError("Product does not exist.")


class DeleteProduct(graphene.Mutation):
    """Mutation for deleting a product."""
    class Arguments:
        product_id = graphene.ID(required=True)

    ok = graphene.String()

    @classmethod
    @staff_member_required
    def mutate(cls, root, info, product_id):
        try:
            product = Product.objects.get(pk=product_id)
            product.delete()
            return DeleteProductPromotions(ok="ok")
        except Product.DoesNotExist:
            raise GraphQLError("Product does not exist.")
