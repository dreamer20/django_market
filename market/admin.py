from django.contrib import admin
from .models import Laptop, Category, Product_code
from .forms import LaptopForm
from django.db import models
from django import forms
# Register your models here.
admin.site.register(Category)
admin.site.register(Product_code)


class LaptopAdmin(admin.ModelAdmin):
    # formfield_overrides = {
    #     models.ForeignKey: {'widget': forms.TextInput}
    # }
    form = LaptopForm


admin.site.register(Laptop, LaptopAdmin)