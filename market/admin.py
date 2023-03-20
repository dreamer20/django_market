from django.contrib import admin
from .models import Laptop, Category, Product_code, Order, Order_items, Television, Desktop
from .forms import ProductForm


class ProductAdmin(admin.ModelAdmin):
    form = ProductForm


admin.site.register(Category)
admin.site.register(Product_code)
admin.site.register(Order)
admin.site.register(Order_items)

admin.site.register(Laptop, ProductAdmin)
admin.site.register(Desktop, ProductAdmin)
admin.site.register(Television, ProductAdmin)
