import django_filters

from .models import ShoppingListItem


class ShoppingListFilter(django_filters.FilterSet):
    class Meta:
        model = ShoppingListItem
        fields = [
            "product",
            "count",
        ]
