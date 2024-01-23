from django.contrib import admin
from .models import Product, ShoppingListItem


# Register your models here.
admin.site.register(Product)
admin.site.register(ShoppingListItem)