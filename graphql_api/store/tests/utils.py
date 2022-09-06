from decimal import Decimal
from django.contrib.auth import get_user_model
from store.models import Collection, Product, Promotion

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

def create_promotion(description='Noruz', discount=20):
    return Promotion.objects.create(
        description=description, discount=discount
    )