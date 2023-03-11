from django.test import TestCase
from django.urls import reverse
from market.models import Laptop, Product_code, Category


def create_laptop():
    category = Category.objects.create(name='laptops')
    product_code = Product_code.objects.create(product_code='020202')
    laptop = Laptop.objects.create(
        product_code=product_code,
        brand='Lenovo',
        model='E-500',
        price=2000,
        count=2,
        category=category,
        screen_size='',
        disk_size=256,
        cpu='',
        gpu='',
        ram_memory=16,
        os=''
    )

    return laptop


class IndexViewTest(TestCase):
    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')


class CategoryViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.category = Category.objects.create(name='laptops')

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('category', kwargs={'category': self.category.name}))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('category', kwargs={'category': self.category.name}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'category.html')


class CartViewTest(TestCase):
    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/cart')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('cart'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('cart'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cart.html')


class CartAddProductViewTest(TestCase):
    def test_view_adds_product_to_cart(self):
        laptop = create_laptop()
        data = {
            'product_code': laptop.product_code.product_code,
            'category': laptop.category.name
        }
        response = self.client.post(reverse('cart_add'), data)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(self.client.session.get('items'), dict)
        self.assertIsInstance(self.client.session['items'].get(laptop.category.name), dict)
        self.assertEqual(len(self.client.session['items'][laptop.category.name]), 1)

    def test_view_adds_few_same_products_to_cart(self):
        laptop = create_laptop()
        data = {
            'product_code': laptop.product_code.product_code,
            'category': laptop.category.name
        }
        response = self.client.post(reverse('cart_add'), data)
        response = self.client.post(reverse('cart_add'), data)
        response = self.client.post(reverse('cart_add'), data)

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(self.client.session.get('items'), dict)
        self.assertIsInstance(self.client.session['items'].get(laptop.category.name), dict)
        self.assertEqual(self.client.session['items'][laptop.category.name][laptop.product_code.product_code], 3)


class CartRemoveProductViewTest(TestCase):
    def test_view_removes_product_from_cart(self):

        laptop = create_laptop()
        data = {
            'product_code': laptop.product_code.product_code,
            'category': laptop.category.name
        }
        response = self.client.post(reverse('cart_add'), data)
        self.assertEqual(response.status_code, 200)

        response = self.client.post(reverse('cart_remove'), data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(self.client.session['items'][laptop.category.name]), 0)


class CartReduceProductCountView(TestCase):
    def test_view_reduces_count_of_product_from_cart(self):
        laptop = create_laptop()
        data = {
            'product_code': laptop.product_code.product_code,
            'category': laptop.category.name
        }
        response = self.client.post(reverse('cart_add'), data)
        response = self.client.post(reverse('cart_add'), data)
        response = self.client.post(reverse('cart_add'), data)
        self.assertEqual(response.status_code, 200)

        response = self.client.post(reverse('cart_reduce'), data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.client.session['items'][laptop.category.name][laptop.product_code.product_code], 2)