from django import forms
from .models import Laptop, Order

CPU_LIST = [(item['cpu'], item['cpu']) for item in Laptop.objects.values('cpu').distinct()]
GPU_LIST = [(item['gpu'], item['gpu']) for item in Laptop.objects.values('gpu').distinct()]
RAM_MEMORY_LIST = [(item['ram_memory'], item['ram_memory']) for item in Laptop.objects.values('ram_memory').distinct()]
SCREEN_SIZE_LIST = [(item['screen_size'], item['screen_size']) for item in Laptop.objects.values('screen_size').distinct()]
DISK_SIZE_LIST = [(item['disk_size'], item['disk_size']) for item in Laptop.objects.values('disk_size').distinct()]
OS_LIST = [(item['os'], item['os']) for item in Laptop.objects.values('os').distinct()]


class MyWidjet(forms.CheckboxSelectMultiple):
    template_name = 'checkbox_select.html'
    option_template_name = 'checkbox_option.html'

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
