from django import forms
from .models import Laptop, Order


class LaptopForm(forms.ModelForm):
    class Meta:
        model = Laptop
        widgets = {
            'product_code': forms.TextInput()
        }
        fields = '__all__'


class OrderForm(forms.ModelForm):

    class Meta:
        common_attrs = {'class': 'form-control'}
        model = Order
        widgets = {
            'adress': forms.TextInput(attrs=common_attrs),
            'client_name': forms.TextInput(attrs=common_attrs),
            'phone_number': forms.TextInput(attrs=common_attrs),
            'email': forms.EmailInput(attrs=common_attrs)
        }
        exclude = ['order_date']
