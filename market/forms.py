from django import forms
from .models import Laptop, Order, Desktop, Television
from .utils import getFieldValueList


class MyWidjet(forms.CheckboxSelectMultiple):
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
    CPU_LIST = getFieldValueList(Laptop, 'cpu')
    GPU_LIST = getFieldValueList(Laptop, 'gpu')
    RAM_MEMORY_LIST = getFieldValueList(Laptop, 'ram_memory')
    SCREEN_SIZE_LIST = getFieldValueList(Laptop, 'screen_size')
    DISK_SIZE_LIST = getFieldValueList(Laptop, 'disk_size')
    OS_LIST = getFieldValueList(Laptop, 'os')

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
        choices=CPU_LIST,
        required=False,
        widget=MyWidjet()
    )

    gpu = forms.MultipleChoiceField(
        label='GPU',
        choices=GPU_LIST,
        required=False,
        widget=MyWidjet()
    )

    ram_memory = forms.MultipleChoiceField(
        label='Ram memory, Gb',
        choices=RAM_MEMORY_LIST,
        required=False,
        widget=MyWidjet()
    )

    screen_size = forms.MultipleChoiceField(
        label='Screen size',
        choices=SCREEN_SIZE_LIST,
        required=False,
        widget=MyWidjet()
    )

    disk_size = forms.MultipleChoiceField(
        label='Disk size, Gb',
        choices=DISK_SIZE_LIST,
        required=False,
        widget=MyWidjet()
    )

    os = forms.MultipleChoiceField(
        label='OS',
        choices=OS_LIST,
        required=False,
        widget=MyWidjet()
    )


class DesktopFilterForm(forms.Form):
    common_attrs = {'class': 'form-control'}
    CPU_LIST = getFieldValueList(Desktop, 'cpu')
    GPU_LIST = getFieldValueList(Desktop, 'gpu')
    DISK_SIZE_LIST = getFieldValueList(Desktop, 'disk_size')
    OS_LIST = getFieldValueList(Desktop, 'os')
    # RAM_MEMORY_LIST = getFieldValueList(Desktop, 'ram_memory')

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
        choices=CPU_LIST,
        required=False,
        widget=MyWidjet()
    )
    gpu = forms.MultipleChoiceField(
        label='GPU',
        choices=GPU_LIST,
        required=False,
        widget=MyWidjet()
    )
    disk_size = forms.MultipleChoiceField(
        label='Disk size',
        choices=DISK_SIZE_LIST,
        required=False,
        widget=MyWidjet()
    )
    os = forms.MultipleChoiceField(
        label='OS',
        choices=OS_LIST,
        required=False,
        widget=MyWidjet()
    )


class TelevisionFilterForm(forms.Form):
    common_attrs = {'class': 'form-control'}
    SCREEN_SIZE_LIST = getFieldValueList(Television, 'screen_size')
    RESOLUTION_LIST = getFieldValueList(Television, 'resolution')
    DISPLAY_TECHNOLOGY_LIST = getFieldValueList(Television, 'display_technology')
    CONNECTIVITY_TECHNOLOGY_LIST = getFieldValueList(Television, 'connectivity_technology')
    PRODUCT_DIMENSIONS_LIST = getFieldValueList(Television, 'product_dimensions')

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
        choices=SCREEN_SIZE_LIST,
        required=False,
        widget=MyWidjet()
    )
    resolution = forms.MultipleChoiceField(
        label='Resolution',
        choices=RESOLUTION_LIST,
        required=False,
        widget=MyWidjet()
    )
    display_technology = forms.MultipleChoiceField(
        label='Display technology',
        choices=DISPLAY_TECHNOLOGY_LIST,
        required=False,
        widget=MyWidjet()
    )
