import django_filters
from django.db.models import Q
from backend.models import ProductInfo

class ProductInfoFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method="filter_search", label="Поиск")
    shop = django_filters.NumberFilter(field_name="shop_id", label="Магазин")
    category = django_filters.NumberFilter(field_name="product__category_id", label="Категория продукта")

    class Meta:
        model = ProductInfo
        fields = ['search', 'shop', 'category']

    def filter_search(self, qs, name, value):
        return qs.filter(
            Q(product__name__icontains=value) | Q(product__model__icontains=value)
        )