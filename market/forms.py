from django import forms
from .models import Laptop


class LaptopForm(forms.ModelForm):
    class Meta:
        model = Laptop
        widgets = {
            'product_code': forms.TextInput()
        }
        fields = '__all__'
