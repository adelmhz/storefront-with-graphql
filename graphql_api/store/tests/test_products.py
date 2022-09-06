import json
from graphene_django.utils.testing import GraphQLTestCase
from graphql_relay import from_global_id
from store.models import Product, Promotion
from .consts import *
from graphql_api.utils import create_collection, create_product, create_promotion, create_user

class PublicProductTest(GraphQLTestCase):
    """Test products for anonymouse users."""
    GRAPHQL_URL = '/graphql'

    def test_query_all_products(self):
        product_1 = create_product()
        product_2 = create_product(title='test product2')
        product_3 = create_product(title='test product3')

        resp = self.query(
            ALL_PRODUCTS_QUERY,
            op_name='allProducts',
        )
        content = json.loads(resp.content)
        products = [item['node'] for item in content['data']['allProducts']['edges']]
        self.assertResponseNoErrors(resp)
        self.assertEqual(len(products), 3)

        for item in products:
            _, product_id = from_global_id(item['id'])
            product_id = int(product_id)
            product = Product.objects.get(pk=product_id)
            self.assertEqual(product_id, product.id)
            self.assertEqual(item['title'], product.title)

    def test_query_product(self):
        product_obj = create_product()

        resp = self.query(
            PRODUCT_QUERY,
            op_name='product',
            variables={'productId': product_obj.id}
        )
        content = json.loads(resp.content)
        product = content['data']['product']
        _, product_id = from_global_id(product['id'])
        product_id = int(product_id)

        self.assertResponseNoErrors(resp)
        self.assertEqual(product_id, product_obj.id)
        self.assertEqual(product['title'], product_obj.title)

    def test_create_product_authenticated_error(self):
        collection_obj = create_collection()
        promotion_1 = create_promotion()
        promotion_2 = create_promotion(description='Tiregan', discount=20)

        resp = self.query(
            CREATE_PRODUCT_MUTATION,
            op_name='createProduct',
            variables={
                'title': 'Test product',
                'slug': 'test-product',
                'unitPrice': '60.50',
                'inventory': 20,
                'collectionId': collection_obj.id,
                'promotions': [promotion_1.id, promotion_2.id]
                }
        )
        content = json.loads(resp.content)

        self.assertEqual(content['errors'][0]['message'],
                         'You do not have permission to perform this action')

    def test_update_product_authenticated_error(self):
        product_obj = create_product()
        promotion_1 = create_promotion()
        promotion_2 = create_promotion(description='Tiregan', discount=20)

        resp = self.query(
            EDIT_PRODUCT_MUTATION,
            op_name='editProduct',
            variables={
                'productId': product_obj.id,
                'title': 'Test product',
                'slug': 'test-product',
                'unitPrice': '60.50',
                'inventory': 20,
                'collectionId': product_obj.collection.id,
                'promotions': [promotion_1.id, promotion_2.id]
                }
        )
        content = json.loads(resp.content)

        self.assertEqual(content['errors'][0]['message'],
                         'You do not have permission to perform this action')

    def test_delete_product_authenticated_error(self):
        product_obj = create_product()

        resp = self.query(
            DELETE_PRODUCT_MUTATION,
            op_name='deleteProduct',
            variables={'productId': product_obj.id}
        )

        content = json.loads(resp.content)

        self.assertEqual(content['errors'][0]['message'],
                         'You do not have permission to perform this action')


class PrivateProductTest(GraphQLTestCase):
    """Tests product for authenticated users."""
    GRAPHQL_URL = '/graphql'

    def setUp(self) -> None:
        super().setUp()
        self.user = create_user()
        self.client.force_login(self.user)

    def test_create_product(self):
        collection_obj = create_collection()
        promotion_1 = create_promotion()
        promotion_2 = create_promotion(description='Tiregan', discount=20)

        resp = self.query(
            CREATE_PRODUCT_MUTATION,
            op_name='createProduct',
            variables={
                'title': 'Test product',
                'slug': 'test-product',
                'unitPrice': '60.50',
                'inventory': 20,
                'collectionId': collection_obj.id,
                'promotions': [promotion_1.id, promotion_2.id]
                }
        )
        content = json.loads(resp.content)
        product = content['data']['createProduct']['product']
        promotions = [item['node'] for item in product['promotions']['edges']]
        collection = product['collection']
        _, collection_id_str = from_global_id(collection['id'])
        collection_id = int(collection_id_str)

        self.assertResponseNoErrors(resp)
        self.assertEqual(product['title'], 'Test product')
        self.assertEqual(product['unitPrice'], '60.50')
        self.assertEqual(collection_obj.id, collection_id)

        for promotion in promotions:
            _, promotion_id = from_global_id(promotion['id'])
            promotion_id = int(promotion_id)
            promotion_obj = Promotion.objects.get(pk=promotion_id)
            self.assertEqual(promotion_obj.id, promotion_id)

    def test_update_product(self):
        product_obj = create_product()
        promotion_1 = create_promotion()
        promotion_2 = create_promotion(description='Tiregan', discount=20)

        resp = self.query(
            EDIT_PRODUCT_MUTATION,
            op_name='editProduct',
            variables={
                'productId': product_obj.id,
                'title': 'Test product',
                'slug': 'test-product',
                'unitPrice': '60.50',
                'inventory': 20,
                'collectionId': product_obj.collection.id,
                'promotions': [promotion_1.id, promotion_2.id]
                }
        )
        content = json.loads(resp.content)
        product = content['data']['editProduct']['product']
        promotions = [item['node'] for item in product['promotions']['edges']]
        collection = product['collection']
        _, collection_id_str = from_global_id(collection['id'])
        collection_id = int(collection_id_str)

        self.assertResponseNoErrors(resp)
        self.assertEqual(product['title'], 'Test product')
        self.assertEqual(product['unitPrice'], '60.50')
        self.assertEqual(product_obj.collection.id, collection_id)

        for promotion in promotions:
            _, promotion_id = from_global_id(promotion['id'])
            promotion_id = int(promotion_id)
            promotion_obj = Promotion.objects.get(pk=promotion_id)
            self.assertEqual(promotion_obj.id, promotion_id)

    def test_delete_product(self):
        product_obj = create_product()

        resp = self.query(
            DELETE_PRODUCT_MUTATION,
            op_name='deleteProduct',
            variables={'productId': product_obj.id}
        )

        content = json.loads(resp.content)

        self.assertResponseNoErrors(resp)
        self.assertEqual(content['data']['deleteProduct']['ok'], True)
        with self.assertRaises(Product.DoesNotExist):
            Product.objects.get(pk=product_obj.id)

    def test_delete_product_promotions(self):
        product_obj = create_product()
        promotion_1 = create_promotion()
        promotion_2 = create_promotion(description='Tiregan', discount=20)
        product_obj.promotions.add(promotion_1)
        product_obj.promotions.add(promotion_2)

        resp = self.query(
            DELETE_PRODUCT_PROMOTIONS_MUTATION,
            op_name='deleteProductPromotions',
            variables={'productId': product_obj.id}
        )

        content = json.loads(resp.content)

        self.assertResponseNoErrors(resp)
        self.assertEqual(content['data']['deleteProductPromotions']['ok'], True)
        self.assertEqual((len(product_obj.promotions.all())), 0)