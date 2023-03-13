from django.contrib import admin
from .models import Laptop, Category, Product_code, Order, Order_items
from .forms import LaptopForm
from django.db import models
from django import forms
# Register your models here.
admin.site.register(Category)
admin.site.register(Product_code)
admin.site.register(Order)
admin.site.register(Order_items)


class LaptopAdmin(admin.ModelAdmin):
    # formfield_overrides = {
    #     models.ForeignKey: {'widget': forms.TextInput}
    # }
    form = LaptopForm


admin.site.register(Laptop, LaptopAdmin)
