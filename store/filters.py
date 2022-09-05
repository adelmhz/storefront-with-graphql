from django_filters.rest_framework import FilterSet, OrderingFilter
from .models import Product, Review, Promotion

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