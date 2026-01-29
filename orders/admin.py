from django.contrib import admin
from .models import Table, Product, ProductType, Order

admin.site.register(Table)
admin.site.register(Product)
admin.site.register(ProductType)
admin.site.register(Order)