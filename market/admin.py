from django.contrib import admin
from .models import Laptop, Category, Product_code, Order, Order_items, Television, Desktop
from .forms import ProductForm
from django.db import models
from django import forms
# Register your models here.
admin.site.register(Category)
admin.site.register(Product_code)
admin.site.register(Order)
admin.site.register(Order_items)


class ProductAdmin(admin.ModelAdmin):
    # formfield_overrides = {
    #     models.ForeignKey: {'widget': forms.TextInput}
    # }
    form = ProductForm


admin.site.register(Laptop, ProductAdmin)
admin.site.register(Desktop, ProductAdmin)
admin.site.register(Television, ProductAdmin)
