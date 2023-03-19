from django import forms
from .models import Laptop, Order, Desktop, Television


def getChoices(Model, field_name):
    return lambda: Model.objects.values_list(field_name, field_name).distinct()


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
        choices=getChoices(Laptop, 'cpu'),
        required=False,
        widget=MyWidjet()
    )

    gpu = forms.MultipleChoiceField(
        label='GPU',
        choices=getChoices(Laptop, 'gpu'),
        required=False,
        widget=MyWidjet()
    )

    ram_memory = forms.MultipleChoiceField(
        label='Ram memory, Gb',
        choices=getChoices(Laptop, 'ram_memory'),
        required=False,
        widget=MyWidjet()
    )

    screen_size = forms.MultipleChoiceField(
        label='Screen size',
        choices=getChoices(Laptop, 'screen_size'),
        required=False,
        widget=MyWidjet()
    )

    disk_size = forms.MultipleChoiceField(
        label='Disk size, Gb',
        choices=getChoices(Laptop, 'disk_size'),
        required=False,
        widget=MyWidjet()
    )

    os = forms.MultipleChoiceField(
        label='OS',
        choices=getChoices(Laptop, 'os'),
        required=False,
        widget=MyWidjet()
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
        choices=getChoices(Desktop, 'cpu'),
        required=False,
        widget=MyWidjet()
    )
    gpu = forms.MultipleChoiceField(
        label='GPU',
        choices=getChoices(Desktop, 'gpu'),
        required=False,
        widget=MyWidjet()
    )
    disk_size = forms.MultipleChoiceField(
        label='Disk size',
        choices=getChoices(Desktop, 'disk_size'),
        required=False,
        widget=MyWidjet()
    )
    os = forms.MultipleChoiceField(
        label='OS',
        choices=getChoices(Desktop, 'os'),
        required=False,
        widget=MyWidjet()
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
        choices=getChoices(Television, 'screen_size'),
        required=False,
        widget=MyWidjet()
    )
    resolution = forms.MultipleChoiceField(
        label='Resolution',
        choices=getChoices(Television, 'resolution'),
        required=False,
        widget=MyWidjet()
    )
    display_technology = forms.MultipleChoiceField(
        label='Display technology',
        choices=getChoices(Television, 'display_technology'),
        required=False,
        widget=MyWidjet()
    )
