import json
from django.contrib.auth import get_user_model
from graphene_django.utils.testing import GraphQLTestCase
from store.models import Collection, Product
from decimal import Decimal
from .consts import *


def create_user(username='test_user', password='test_user1234', is_staff=True):
    return get_user_model().objects.create(
        username=username, password=password, is_staff=is_staff)


def create_collection(title='Test collection'):
    collection = Collection.objects.create(
        title='Test collection'
    )

    return collection


def create_product(
        title='test product', unit_price=Decimal(65.00),
        inventory=40, collection=None, promotions=None):
    collection = create_collection()

    product = Product()
    product.title = 'test product'
    product.unit_price = Decimal(65.00)
    product.inventory = 30
    product.collection = collection
    product.save()

    return product


class PublicCollectionTests(GraphQLTestCase):
    """Tests collections for anonymouse users. """
    GRAPHQL_URL = '/graphql'

    def test_query_collections(self):
        collection = Collection.objects.create(
            title='Test'
        )

        resp = self.query(
            COLLECTION_QUERY,
            op_name='collections',
            variables={'id': float(collection.id)}
        )
        content = json.loads(resp.content)

        self.assertResponseNoErrors(resp)
        self.assertEqual(len(content['data']['collections']['edges']), 1)

    def test_create_collection_authenticated_error(self):
        product = create_product()

        resp = self.query(
            CREATE_COLLECTION_MUTATION,
            op_name='createCollection',
            variables={'title': 'Test collection',
                       'featuredProductId': product.id}
        )
        content = json.loads(resp.content)

        self.assertEqual(content['errors'][0]['message'],
                         'You do not have permission to perform this action')

    def test_updating_collection_authenticated_error(self):
        collection = create_collection()

        resp = self.query(
            EDIT_COLLECTION_MUTATION,
            op_name='editCollection',
            variables={'collectionId': collection.id, 'title': 'Test collection'}
        )
        content = json.loads(resp.content)

        self.assertEqual(content['errors'][0]['message'],
                         'You do not have permission to perform this action')

    def test_delete_collection_authenticated_error(self):
        collection = create_collection()

        resp = self.query(
            DELETE_COLLECTION_MUTATION,
            op_name='deleteCollection',
            variables={'collectionId': collection.id}
        )
        content = json.loads(resp.content)

        self.assertEqual(content['errors'][0]['message'],
                         'You do not have permission to perform this action')

class PrivateCollectionTests(GraphQLTestCase):
    """Tests collections for authenticated users."""
    GRAPHQL_URL = '/graphql'

    def setUp(self) -> None:
        super().setUp()
        self.user = create_user()
        self.client.force_login(self.user)

    def test_create_collection(self):
        product = create_product()

        resp = self.query(
            CREATE_COLLECTION_MUTATION,
            op_name='createCollection',
            variables={'title': 'Test collection',
                       'featuredProductId': product.id}
        )
        content = json.loads(resp.content)

        self.assertResponseNoErrors(resp)
        self.assertIsNotNone(content['data']['createCollection']['collection'])

    def test_update_collection(self):
        collection = create_collection()

        resp = self.query(
            EDIT_COLLECTION_MUTATION,
            op_name='editCollection',
            variables={'collectionId': collection.id, 'title': 'Test collection'}
        )
        content = json.loads(resp.content)

        self.assertResponseNoErrors(resp)
        self.assertIsNotNone(content['data']['editCollection']['collection'])

    def test_delete_collection(self):
        collection = create_collection()

        resp = self.query(
            DELETE_COLLECTION_MUTATION,
            op_name='deleteCollection',
            variables={'collectionId': collection.id}
        )
        content = json.loads(resp.content)

        self.assertResponseNoErrors(resp)
        self.assertEqual(content['data']['deleteCollection']['ok'], True)