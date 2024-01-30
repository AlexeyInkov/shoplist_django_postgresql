from django.forms import ModelForm
from .models import ShoppingListItem, Product


class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = "name", "price"


class ShoppingListForm(ModelForm):
    class Meta:
        model = ShoppingListItem
        fields = "product", "count"
