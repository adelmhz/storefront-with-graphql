import json
from graphene_django.utils.testing import GraphQLTestCase
from graphql_relay import from_global_id
from core.models import User
from .consts import *
from graphql_api.utils import create_user, create_superuser

class PublicUserTest(GraphQLTestCase):
    """Test users for anonymouse users."""
    GRAPHQL_URL = '/graphql'

    def test_me_authenticated_error(self):
        resp = self.query(
            ME_QUERY,
            op_name='me'
        )
        content = json.loads(resp.content)

        self.assertResponseHasErrors(resp)
        self.assertEqual(content['errors'][0]['message'],
                         'You do not have permission to perform this action')

    def test_create_user(self):
        resp = self.query(
            CREATE_USER_MUTATION,
            op_name='createUser',
            variables={
                "email": "adfdsf@gmail.com", "username": "test",
                "password": "adelTest123", "firstName": "Test",
                "lastName": "Unit", "isStaff": True
            }
        )
        content = json.loads(resp.content)

        self.assertResponseHasErrors(resp)
        self.assertEqual(content['errors'][0]['message'],
                         'You do not have permission to perform this action')


class PrivateUserTest(GraphQLTestCase):
    """Test users query and mutations for superuser. """
    GRAPHQL_URL = '/graphql'

    def setUp(self) -> None:
        super().setUp()
        self.user = create_superuser()
        self.client.force_login(self.user)

    def test_me(self):
        resp = self.query(
            ME_QUERY,
            op_name='me'
        )
        content = json.loads(resp.content)
        user = content['data']['me']

        self.assertResponseNoErrors(resp)
        self.assertEqual(user['username'], self.user.username)
        self.assertTrue(user['isSuperuser'])



    def test_create_user(self):
        resp = self.query(
            CREATE_USER_MUTATION,
            op_name='createUser',
            variables={
                "email": "adfdsf@gmail.com", "username": "test",
                "password": "adelTest123", "firstName": "Test",
                "lastName": "Unit", "isStaff": True
            }
        )
        content = json.loads(resp.content)
        user = content['data']['createUser']['user']
        _, user_id_str = from_global_id(user['id'])
        user_id = int(user_id_str)
        user_obj = User.objects.get(pk=user_id)

        self.assertResponseNoErrors(resp)
        self.assertEqual(user_id, user_obj.id)
        self.assertEqual("adfdsf@gmail.com", user_obj.email)
        self.assertEqual("test", user_obj.username)
        self.assertEqual("Test", user_obj.first_name)
        self.assertEqual("Unit", user_obj.last_name)
        self.assertTrue(user_obj.is_staff)

