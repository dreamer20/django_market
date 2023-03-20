from itertools import chain
from operator import attrgetter
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse
from django.core.paginator import Paginator
from django.views.generic import ListView, TemplateView
from django.contrib.postgres.search import SearchVector
from .models import Laptop, Product_code, Category, Order_items
from . import models, forms
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
        FilterForm = getattr(forms, f'{category[:-1].title()}FilterForm')
        form = FilterForm(self.request.GET)
        items = Product.objects.all()

        if form.is_valid():
            if form.cleaned_data['price_min'] is not None:
                items = Product.objects.filter(price__gte=form.cleaned_data['price_min'])
            if form.cleaned_data['price_max'] is not None:
                items = Product.objects.filter(price__lte=form.cleaned_data['price_max'])
            for key, value in form.cleaned_data.items():
                if key not in ('price_min', 'price_max'):
                    if len(value) > 0:
                        option = {f'{key}__in': value}
                        items = Product.objects.filter(**option)
        return items

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.kwargs['category']
        category = self.kwargs['category']
        items = self.request.session.get('items')
        if items is not None:
            context['product_codes'] = items.keys()
        FilterForm = getattr(forms, f'{category[:-1].title()}FilterForm')
        form = FilterForm(self.request.GET)
        context['form'] = form
        context['isFilterFormCollapsed'] = self.request.session.get('isFilterFormCollapsed')
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

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        items = request.session.get('items')

        if items is None:
            return redirect('cart')

        if form.is_valid():
            order = form.save()
            product_codes = Product_code.objects.filter(product_code__in=items.keys())
            for product_code in product_codes:
                product_count = items[product_code.product_code]
                Order_items.objects.create(
                    order=order,
                    product_code=product_code,
                    count=product_count
                )
            return redirect(reverse('order_success'))

        return render(request, self.template_name)


class OrderSuccessView(TemplateView):
    template_name = 'order_success.html'


class ProdcutDetailView(TemplateView):
    template_name = 'product_detail.html'

    def get(self, request, *args, **kwargs):
        context = dict()
        category_name = kwargs['category']
        product_code = kwargs['product_code']
        items = request.session.get('items')
        if items is not None:
            if items.get(product_code) is not None:
                context['product_code'] = product_code
        Product = getattr(models, category_name[:-1].title())
        product = Product.objects.get(product_code=product_code)
        context['product'] = product
        return render(request, self.template_name, context)


class PersonalSettingsView(TemplateView):
    def get(self, request, *args, **kwargs):
        isFilterFormCollapsed = request.GET.get('filter_form')

        if isFilterFormCollapsed == 'collapsed':
            request.session['isFilterFormCollapsed'] = True
        elif isFilterFormCollapsed == 'expanded':
            request.session['isFilterFormCollapsed'] = False

        return HttpResponse(status=200)


class SearchView(TemplateView):
    template_name = 'search.html'
    paginate_by = 10

    def get(self, request, *args, **kwargs):
        results = list()
        context = dict()

        searchString = self.request.GET.get('q')
        page_number = self.request.GET.get('page')
        items = self.request.session.get('items')
        context['q'] = self.request.GET.get('q')

        category = Category.objects.filter(name=searchString).first()

        if items is not None:
            context['product_codes'] = items.keys()

        if category:
            Product = getattr(models, category.name[:-1].title())
            results = Product.objects.all().order_by('product_code')
            paginator = Paginator(results, self.paginate_by)
            page_obj = paginator.get_page(page_number)
            context['page_obj'] = page_obj

            return render(request, 'search.html', context)

        categories = Category.objects.all()
        for category in categories:
            Product = getattr(models, category.name[:-1].title())
            s = SearchVector('brand', 'model', 'description')
            results.append(Product.objects.annotate(search=s).filter(search=searchString))
            products = sorted(chain(*results), key=attrgetter('brand'))

        paginator = Paginator(products, self.paginate_by)
        page_obj = paginator.get_page(page_number)
        context['page_obj'] = page_obj

        return render(request, 'search.html', context)
