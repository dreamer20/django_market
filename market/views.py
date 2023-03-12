from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse
from django.views.generic import ListView, TemplateView
from .models import Laptop, Product_code, Category
from . import models
from .forms import OrderForm
# Create your views here.


class IndexView(ListView):
    template_name = 'index.html'
    context_object_name = 'item_list'

    def get_queryset(self):
        return Laptop.objects.all()


class CategoryView(ListView):
    template_name = 'category.html'
    context_object_name = 'item_list'

    def get_queryset(self):
        category = self.kwargs['category']

        Product = getattr(models, category[:-1].title())
        # if category == 'desktops':
        #     items = Laptop.objects.all()
        # elif category == 'laptops':
        #     items = Laptop.objects.all()
        items = Product.objects.all()
        return items

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.kwargs['category']
        items = self.request.session.get('items')
        if items is not None:
            context['product_codes'] = items.keys()
        return context


class CartView(TemplateView):
    template_name = 'cart.html'

    def get(self, request, *args, **kwargs):
        products = list()
        total_price = 0
        context = dict()
        items = request.session.get('items')

        if items is not None:
            product_codes = Product_code.objects.filter(product_code__in=items.keys())
            for product_code in product_codes:
                categories = Category.objects.all()
                for category in categories:
                    product = getattr(product_code, category.name[:-1], None)
                    if product is not None:
                        product_count = items[product_code.product_code]
                        products.append((product_count, product))
                        total_price += product_count * product.price
                        break
            context = {
                'products': products,
                'total_price': total_price,
            }

        return render(request, self.template_name, context=context)


class CartAddProductView(TemplateView):
    def post(self, request, *args, **kwargs):
        product_code = request.POST['product_code']

        if request.session.get('items') is None:
            request.session['items'] = dict()

        if request.session['items'].get(product_code) is None:
            request.session['items'][product_code] = 1
            request.session['items_count'] = len(request.session['items'])
        else:
            request.session['items'][product_code] += 1
        request.session.modified = True

        return HttpResponse(status=200)


class CartReduceProductCountView(TemplateView):
    def post(self, request, *args, **kwargs):
        product_code = request.POST['product_code']

        if request.session.get('items') is not None:
            if request.session['items'][product_code] > 1:
                request.session['items'][product_code] -= 1
        request.session.modified = True

        return HttpResponse(product_code)


class CartRemoveProductView(TemplateView):
    def post(self, request, *args, **kwargs):
        product_code = request.POST['product_code']

        if request.session.get('items') is not None:
            del request.session['items'][product_code]
            request.session['items_count'] = len(request.session['items'])

        request.session.modified = True

        return HttpResponse(product_code)


class OrderView(TemplateView):
    template_name = 'order.html'
    form_class = OrderForm

    def get(self, request, *args, **kwargs):
        items = request.session.get('items')
        total_price = 0

        if items is None or len(items) == 0:
            return redirect(reverse('cart'))

        form = self.form_class()
        items = request.session.get('items')

        if items is not None:
            product_codes = Product_code.objects.filter(product_code__in=items.keys())
            for product_code in product_codes:
                categories = Category.objects.all()
                for category in categories:
                    product = getattr(product_code, category.name[:-1], None)
                    if product is not None:
                        product_count = items[product_code.product_code]
                        total_price += product_count * product.price
                        break
        context = {
            'form': form,
            'total_price': total_price
        }
        return render(request, self.template_name, context)
