from django_filters.rest_framework import FilterSet, OrderingFilter
from store.models import Product, Review, Promotion

class ProductFilter(FilterSet):
    class Meta:
        model = Product
        fields = {
            'collection_id': ['exact'],
            'unit_price': ['gt', 'lt']
        }
        order_by = OrderingFilter(
            fields=(
                ('unit_price', 'last_update', 'title')
            )
        )

class ReviewFilter(FilterSet):
    class Meta:
        model = Review
        fields = {
            'date': ['gt', 'lt']
        }
        order_by = OrderingFilter(
        fields=(
            ('date'),
        )
    )

class PromotionFilter(FilterSet):
    class Meta:
        model = Promotion
        fields = {
            'description': ['icontains'],
        }
        order_by = OrderingFilter(
            fields=(
                ('discount'),
            )
        )