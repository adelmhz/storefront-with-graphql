import json
from decimal import Decimal
from graphene_django.utils.testing import GraphQLTestCase
from graphql_relay import from_global_id
from store.models import Collection, Product, Promotion
from .consts import *
from .utils import create_collection, create_product, create_promotion, create_user


class PublicPromotionTest(GraphQLTestCase):
    """Test promotions for anonymouse users."""
    GRAPHQL_URL = '/graphql'

    def test_all_promotions_query(self):
        promotion_1 = create_promotion()
        promotion_2 = create_promotion(description='Test promotion')

        resp = self.query(
            ALL_PROMOTIONS_QUERY,
            op_name='allPromotions'
        )
        content = json.loads(resp.content)
        promotions = [item['node']
                      for item in content['data']['allPromotions']['edges']]

        self.assertResponseNoErrors(resp)
        self.assertEqual(len(promotions), 2)
        for promotion in promotions:
            _, promotion_id_str = from_global_id(promotion['id'])
            promotion_id = int(promotion_id_str)
            promotion_obj = Promotion.objects.get(pk=promotion_id)

            self.assertEqual(promotion_id, promotion_obj.id)
            self.assertEqual(promotion['description'],
                             promotion_obj.description)

    def test_promotion_query(self):
        promotion_1 = create_promotion()

        resp = self.query(
            PROMOTION_QUERY,
            op_name='promotion',
            variables={'promotionId': promotion_1.id}
        )
        content = json.loads(resp.content)
        promotion = content['data']['promotion']
        _, promotion_id_str = from_global_id(promotion['id'])
        promotion_id = int(promotion_id_str)
        promotion_obj = Promotion.objects.get(pk=promotion_id)
        self.assertEqual(promotion_id, promotion_obj.id)

        self.assertResponseNoErrors(resp)
        self.assertEqual(promotion['description'], promotion_obj.description)
        self.assertEqual(promotion['discount'], promotion_obj.discount)

    def test_create_promotion_authenticated_error(self):
        resp = self.query(
            CREATE_PROMOTION_MUTATION,
            op_name='createPromotion',
            variables={'description': 'Test Description', 'discount': 30.5}
        )
        content = json.loads(resp.content)

        self.assertEqual(content['errors'][0]['message'],
                         'You do not have permission to perform this action')

    def test_update_promotion_authenticated_error(self):
        promotion_obj = create_promotion()

        resp = self.query(
            UPDATE_PROMOTION_MUTATION,
            op_name='editPromotion',
            variables={
                'promotionId': promotion_obj.id,
                'description': 'Edited description',
                }
        )
        content = json.loads(resp.content)

        self.assertEqual(content['errors'][0]['message'],
                         'You do not have permission to perform this action')


    def test_delete_promotion_authenticated_error(self):
        promotion_obj = create_promotion()
        resp = self.query(
            DELETE_PROMOTION_MUTATION,
            op_name='deletePromotion',
            variables={
                'promotionId': promotion_obj.id,
                }
        )
        content = json.loads(resp.content)

        self.assertEqual(content['errors'][0]['message'],
                         'You do not have permission to perform this action')


class PrivatePromotionTest(GraphQLTestCase):
    """Test promotions for authenticated users."""
    GRAPHQL_URL = '/graphql'

    def setUp(self) -> None:
        super().setUp()
        self.user = create_user()
        self.client.force_login(self.user)

    def test_create_promotion(self):
        resp = self.query(
            CREATE_PROMOTION_MUTATION,
            op_name='createPromotion',
            variables={'description': 'Test Description', 'discount': 30.5}
        )
        content = json.loads(resp.content)
        promotion = content['data']['createPromotion']['promotion']

        self.assertResponseNoErrors(resp)
        self.assertEqual(promotion['description'], 'Test Description')
        self.assertEqual(promotion['discount'], 30.5)

    def test_update_promotion(self):
        promotion_obj = create_promotion()

        resp = self.query(
            UPDATE_PROMOTION_MUTATION,
            op_name='editPromotion',
            variables={
                'promotionId': promotion_obj.id,
                'description': 'Edited description',
                }
        )
        content = json.loads(resp.content)
        promotion = content['data']['editPromotion']['promotion']
        promotion_obj.refresh_from_db()

        self.assertResponseNoErrors(resp)
        self.assertEqual(promotion['description'], promotion_obj.description)

    def test_delete_promotion(self):
        promotion_obj = create_promotion()
        resp = self.query(
            DELETE_PROMOTION_MUTATION,
            op_name='deletePromotion',
            variables={
                'promotionId': promotion_obj.id,
                }
        )
        content = json.loads(resp.content)

        self.assertResponseNoErrors(resp)
        self.assertEqual(content['data']['deletePromotion']['ok'], True)
        with self.assertRaises(Promotion.DoesNotExist):
            Promotion.objects.get(pk=promotion_obj.id)