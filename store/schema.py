import graphene
from graphene_django.filter import DjangoFilterConnectionField
from graphql_jwt.decorators import staff_member_required, login_required
from django.db import transaction
from .models import Product, Collection, Review, Cart, Promotion
from .types import CollectionType


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