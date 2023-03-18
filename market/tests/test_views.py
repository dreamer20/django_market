from django.test import TestCase
from django.urls import reverse
from market.models import Laptop, Product_code, Category


def create_laptop(product_code='020202', price=2000, brand='Lenovo'):
    category = Category.objects.filter(name='laptops').first()

    if category is None:
        category = Category.objects.create(name='laptops')

    product_code = Product_code.objects.create(product_code=product_code)
    laptop = Laptop.objects.create(
        product_code=product_code,
        product_image='',
        brand=brand,
        model='E-500',
        price=price,
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
        response = self.client.get('/cart/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('cart'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('cart'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cart.html')

    def test_view_shows_cart_with_items(self):
        laptop = create_laptop()
        s = self.client.session
        s['items'] = dict()
        s['items'][laptop.product_code.product_code] = 1
        s.save()
        response = self.client.get(reverse('cart'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['products']), 1)


class CartAddProductViewTest(TestCase):
    def test_view_adds_product_to_cart(self):
        laptop = create_laptop()
        data = {
            'product_code': laptop.product_code.product_code,
        }
        response = self.client.post(reverse('cart_add'), data)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(self.client.session.get('items'), dict)
        self.assertEqual(len(self.client.session['items']), 1)

    def test_view_has_items_count_in_context(self):
        laptop = create_laptop()
        data = {
            'product_code': laptop.product_code.product_code,
        }
        response = self.client.post(reverse('cart_add'), data)
        self.assertEqual(response.status_code, 200)

        response = self.client.get(reverse('cart'))
        self.assertEqual(response.context['items_count'], 1)

    def test_view_adds_few_same_products_to_cart(self):
        laptop = create_laptop()
        data = {
            'product_code': laptop.product_code.product_code,
        }
        response = self.client.post(reverse('cart_add'), data)
        response = self.client.post(reverse('cart_add'), data)
        response = self.client.post(reverse('cart_add'), data)

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(self.client.session.get('items'), dict)
        self.assertEqual(self.client.session['items'][laptop.product_code.product_code], 3)


class CartRemoveProductViewTest(TestCase):
    def test_view_removes_product_from_cart(self):

        laptop = create_laptop()
        data = {
            'product_code': laptop.product_code.product_code,
        }
        response = self.client.post(reverse('cart_add'), data)
        self.assertEqual(response.status_code, 200)

        response = self.client.post(reverse('cart_remove'), data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(self.client.session['items']), 0)


class CartReduceProductCountViewTest(TestCase):
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
        self.assertEqual(self.client.session['items'][laptop.product_code.product_code], 2)


class OrderViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.laptop = create_laptop()
        cls.laptop2 = create_laptop('010101', 1500)

    def setUp(self):
        session = self.client.session
        session['items'] = dict()
        session['items'][self.laptop.product_code.product_code] = 1
        session['items'][self.laptop2.product_code.product_code] = 2
        session.save()

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/cart/order/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('order'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('order'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'order.html')

    def test_view_redurects_if_cart_is_empty(self):
        session = self.client.session
        session.clear()
        session.save()

        response = self.client.get(reverse('order'))
        self.assertRedirects(response, reverse('cart'))

    def test_view_context_has_correct_total_price(self):
        response = self.client.get(reverse('order'))
        self.assertEqual(response.status_code, 200)
        laptopCount = self.client.session['items'][self.laptop.product_code.product_code]
        laptop2Count = self.client.session['items'][self.laptop2.product_code.product_code]
        expectedPrice = self.laptop.price * laptopCount + self.laptop2.price * laptop2Count
        self.assertEqual(response.context['total_price'], expectedPrice)


class ProductDetailViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.laptop = create_laptop()
        cls.laptop2 = create_laptop('010101', 1500)

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get(f'/category/laptops/{self.laptop.product_code.product_code}/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        argumets = {
            'category': 'laptops',
            'product_code': self.laptop.product_code.product_code
        }
        response = self.client.get(reverse('product_detail', kwargs=argumets))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        argumets = {
            'category': 'laptops',
            'product_code': self.laptop.product_code.product_code
        }
        response = self.client.get(reverse('product_detail', kwargs=argumets))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'product_detail.html')


class PersonalSettingsViewTest(TestCase):
    def test_view_saves_filter_form_status_in_session(self):
        response = self.client.get(reverse('personal_settings') + '?filter_form=collapsed')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(self.client.session['isFilterFormCollapsed'])

    def test_view_saves_filter_form_status_in_session_as_expanded(self):
        response = self.client.get(reverse('personal_settings') + '?filter_form=expanded')
        self.assertEqual(response.status_code, 200)
        self.assertFalse(self.client.session['isFilterFormCollapsed'])


class SearchViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.laptop = create_laptop()
        cls.laptop2 = create_laptop('010101', 1500, brand='Samsung')

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/search/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('search'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('search'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'search.html')

    def test_view_gets_searched_products(self):
        response = self.client.get(reverse('search') + '?q=laptops')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['page_obj'].object_list), 2)

        response = self.client.get(reverse('search') + '?q=Lenovo')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['page_obj'].object_list), 1)
