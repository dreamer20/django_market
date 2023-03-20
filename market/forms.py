from django import forms
from .models import Laptop, Order, Desktop, Television
from .utils import get_filter_choices


class CustomCheckboxSelectMultiple(forms.CheckboxSelectMultiple):
    template_name = 'checkbox_select.html'
    option_template_name = 'checkbox_option.html'


class ProductForm(forms.ModelForm):
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


class LaptopFilterForm(forms.Form):
    common_attrs = {'class': 'form-control'}

    price_min = forms.IntegerField(
        min_value=0,
        widget=forms.NumberInput(common_attrs),
        required=False
    )

    price_max = forms.IntegerField(
        min_value=0,
        widget=forms.NumberInput(common_attrs),
        required=False
    )
    cpu = forms.MultipleChoiceField(

        label='Processor',
        choices=get_filter_choices(Laptop, 'cpu'),
        required=False,
        widget=CustomCheckboxSelectMultiple()
    )

    gpu = forms.MultipleChoiceField(
        label='GPU',
        choices=get_filter_choices(Laptop, 'gpu'),
        required=False,
        widget=CustomCheckboxSelectMultiple()
    )

    ram_memory = forms.MultipleChoiceField(
        label='Ram memory, Gb',
        choices=get_filter_choices(Laptop, 'ram_memory'),
        required=False,
        widget=CustomCheckboxSelectMultiple()
    )

    screen_size = forms.MultipleChoiceField(
        label='Screen size',
        choices=get_filter_choices(Laptop, 'screen_size'),
        required=False,
        widget=CustomCheckboxSelectMultiple()
    )

    disk_size = forms.MultipleChoiceField(
        label='Disk size, Gb',
        choices=get_filter_choices(Laptop, 'disk_size'),
        required=False,
        widget=CustomCheckboxSelectMultiple()
    )

    os = forms.MultipleChoiceField(
        label='OS',
        choices=get_filter_choices(Laptop, 'os'),
        required=False,
        widget=CustomCheckboxSelectMultiple()
    )


class DesktopFilterForm(forms.Form):
    common_attrs = {'class': 'form-control'}

    price_min = forms.IntegerField(
        min_value=0,
        widget=forms.NumberInput(common_attrs),
        required=False
    )

    price_max = forms.IntegerField(
        min_value=0,
        widget=forms.NumberInput(common_attrs),
        required=False
    )

    cpu = forms.MultipleChoiceField(
        label='Processor',
        choices=get_filter_choices(Desktop, 'cpu'),
        required=False,
        widget=CustomCheckboxSelectMultiple()
    )

    gpu = forms.MultipleChoiceField(
        label='GPU',
        choices=get_filter_choices(Desktop, 'gpu'),
        required=False,
        widget=CustomCheckboxSelectMultiple()
    )

    disk_size = forms.MultipleChoiceField(
        label='Disk size',
        choices=get_filter_choices(Desktop, 'disk_size'),
        required=False,
        widget=CustomCheckboxSelectMultiple()
    )

    os = forms.MultipleChoiceField(
        label='OS',
        choices=get_filter_choices(Desktop, 'os'),
        required=False,
        widget=CustomCheckboxSelectMultiple()
    )


class TelevisionFilterForm(forms.Form):
    common_attrs = {'class': 'form-control'}

    price_min = forms.IntegerField(
        min_value=0,
        widget=forms.NumberInput(common_attrs),
        required=False
    )

    price_max = forms.IntegerField(
        min_value=0,
        widget=forms.NumberInput(common_attrs),
        required=False
    )

    screen_size = forms.MultipleChoiceField(
        label='Screen size',
        choices=get_filter_choices(Television, 'screen_size'),
        required=False,
        widget=CustomCheckboxSelectMultiple()
    )

    resolution = forms.MultipleChoiceField(
        label='Resolution',
        choices=get_filter_choices(Television, 'resolution'),
        required=False,
        widget=CustomCheckboxSelectMultiple()
    )

    display_technology = forms.MultipleChoiceField(
        label='Display technology',
        choices=get_filter_choices(Television, 'display_technology'),
        required=False,
        widget=CustomCheckboxSelectMultiple()
    )
