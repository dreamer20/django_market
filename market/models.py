from django.db import models
from django.core import validators
from .validators import validate_price
from tinymce import models as tinymce_models
from django.utils import timezone


class Category(models.Model):
    name = models.CharField(max_length=300)
    image = models.ImageField(upload_to='category_images/', blank=True)

    def __str__(self):
        return self.name


class Product_code(models.Model):
    product_code = models.CharField(
        max_length=6,
        validators=[validators.MinLengthValidator(limit_value=6)],
        unique=True,
    )

    def __str__(self):
        return self.product_code


class Product(models.Model):
    class Meta:
        abstract = True

    product_code = models.OneToOneField(
        Product_code,
        on_delete=models.CASCADE,
        to_field='product_code',
        primary_key=True
    )
    brand = models.CharField(max_length=300)
    model = models.CharField(max_length=300)
    product_image = models.ImageField(upload_to='product_images/', blank=True)
    price = models.FloatField(validators=[validate_price])
    count = models.IntegerField(
        validators=[validators.MinValueValidator(limit_value=0)],
        default=0
    )
    description = tinymce_models.HTMLField(default='', blank=True)
    category = models.ForeignKey(
        Category,
        models.SET_NULL,
        blank=True,
        null=True
    )

    def __str__(self):
        return f'{self.brand}: {self.model}'


class Order(models.Model):
    adress = models.CharField(max_length=300)
    client_name = models.CharField(max_length=300)
    phone_number = models.CharField(max_length=12)
    email = models.EmailField(blank=True, null=True)
    order_date = models.DateTimeField(default=timezone.now)


class Order_items(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE
    )
    product_code = models.ForeignKey(
        Product_code,
        on_delete=models.CASCADE,
        to_field='product_code',
    )
    count = models.IntegerField()

    def __str__(self):
        return f'{self.order.client_name}: {self.product_code.laptop.brand}'


class Laptop(Product):
    screen_size = models.CharField(max_length=100, blank=True)
    disk_size = models.IntegerField(blank=True)
    cpu = models.CharField(max_length=300, blank=True)
    gpu = models.CharField(max_length=300, blank=True)
    ram_memory = models.IntegerField(blank=True)
    os = models.CharField(max_length=100, blank=True)


class Desktop(Product):
    disk_size = models.IntegerField(blank=True)
    cpu = models.CharField(max_length=300, blank=True)
    gpu = models.CharField(max_length=300, blank=True)
    os = models.CharField(max_length=100, blank=True)


class Television(Product):
    screen_size = models.CharField(max_length=100, blank=True)
    refresh_rate = models.IntegerField(blank=True)
    resolution = models.CharField(max_length=300, blank=True)
    display_technology = models.CharField(max_length=300, blank=True)
    connectivity_technology = models.CharField(max_length=300, blank=True)
    product_dimensions = models.CharField(max_length=300, blank=True)
