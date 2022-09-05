import graphene
from graphene_django.filter import DjangoFilterConnectionField
from graphql_jwt.decorators import staff_member_required, login_required
from django.db import transaction
from .models import Product, Collection, Review, Cart, Promotion
from .types import CollectionType, ProductType
from .filters import ProductFilter


class CollectionQuery(graphene.ObjectType):
    collection = DjangoFilterConnectionField(CollectionType)


class CreateCollection(graphene.Mutation):
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
            featured_product = Product.objects.get(pk=featured_product_id)
            collection.featured_product = featured_product
        collection.save()

        return CreateCollection(collection=collection)


class EditCollection(graphene.Mutation):
    class Arguments:
        collection_id = graphene.ID(required=True)
        title = graphene.String(required=True)
        featured_product_id = graphene.ID()

    collection = graphene.Field(CollectionType)

    @classmethod
    @staff_member_required
    def mutate(cls, root, info, title, collection_id, featured_product_id=None):
        collection = Collection.objects.get(pk=collection_id)
        collection.title = title
        if featured_product_id:
            featured_product = Product.objects.get(pk=featured_product_id)
            collection.featured_product = featured_product
        collection.save()

        return CreateCollection(collection=collection)


class DeleteCollection(graphene.Mutation):
    class Arguments:
        collection_id = graphene.ID(required=True)

    ok = graphene.Boolean()

    @classmethod
    @staff_member_required
    def mutate(cls, root, info, collection_id):
        collection = Collection.objects.get(pk=collection_id)
        collection.delete()

        return DeleteCollection(ok=True)


class CollectionMutation(graphene.ObjectType):
    create_collection = CreateCollection.Field()
    edit_collection = EditCollection.Field()
    delete_collection = DeleteCollection.Field()


class ProductQuery(graphene.ObjectType):
    all_products = DjangoFilterConnectionField(
        ProductType, filterset_class=ProductFilter)
    product = graphene.Field(
        ProductType, product_id=graphene.ID(required=True))

    def resolve_product(root, info, product_id):
        try:
            return Product.objects.get(pk=product_id)
        except Product.DoesNotExist:
            return None


class CreateProduct(graphene.Mutation):
    class Arguments:
        title = graphene.String(required=True)
        slug = graphene.String(required=True)
        description = graphene.String()
        unit_price = graphene.Decimal(required=True)
        inventory = graphene.Int(required=True)
        collection_id = graphene.ID(required=True)
        promotions = graphene.List(graphene.Int)

    product = graphene.Field(ProductType)
    response = graphene.String()

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
                return CreateProduct(product=None, response="collection does not exist.")

            if promotions:
                for promotion_id in promotions:
                    try:
                        promotion = Promotion.objects.get(pk=promotion_id)
                        product.promotions.add(promotion)
                    except Promotion.DoesNotExist:
                        return CreateProduct(
                            product=None,
                            response=f"promotion id {promotion_id} does not exist.")

            return CreateProduct(product=product)


class EditProduct(graphene.Mutation):
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
    response = graphene.String()

    @classmethod
    @staff_member_required
    def mutate(cls, root, info, **kwargs):
        print("\n\n\n\n")
        product_id = kwargs.pop('product_id', None)
        collection_id = kwargs.pop('collection_id', None)
        promotions = kwargs.pop('promotions', None)

        with transaction.atomic():
            try:
                product = Product.objects.get(pk=product_id)
            except Product.DoesNotExist:
                return CreateProduct(product=None, response="Product does not exist.")

            for attr, value in kwargs.items():
                setattr(product, attr, value)

            if collection_id:
                try:
                    collection = Collection.objects.get(pk=collection_id)
                    product.collection = collection
                except Collection.DoesNotExist:
                    return CreateProduct(product=None, response="collection does not exist.")

            if promotions:
                for promotion_id in promotions:
                    try:
                        promotion = Promotion.objects.get(pk=promotion_id)
                        product.promotions.add(promotion)
                    except Promotion.DoesNotExist:
                        return CreateProduct(
                            product=None,
                            response=f"promotion id {promotion_id} does not exist.")

        return CreateProduct(product=product, response='ok')


class DeleteProductPromotions(graphene.Mutation):
    class Arguments:
        product_id = graphene.ID(required=True)

    response = graphene.String()

    @classmethod
    @staff_member_required
    def mutate(cls, root, info, product_id):
        try:
            product = Product.objects.get(pk=product_id)
            product.promotions.clear()
            return DeleteProductPromotions(response="ok")
        except Product.DoesNotExist:
            return DeleteProductPromotions(response="Product does not exist.")


class DeleteProduct(graphene.Mutation):
    class Arguments:
        product_id = graphene.ID(required=True)

    response = graphene.String()

    @classmethod
    @staff_member_required
    def mutate(cls, root, info, product_id):
        try:
            product = Product.objects.get(pk=product_id)
            product.delete()
            return DeleteProductPromotions(response="ok")
        except Product.DoesNotExist:
            return DeleteProductPromotions(response="Product does not exist.")


class ProductMutation(graphene.ObjectType):
    create_product = CreateProduct.Field()
    edit_product = EditProduct.Field()
    delete_product_promotions = DeleteProductPromotions.Field()
    delete_product = DeleteProduct.Field()
