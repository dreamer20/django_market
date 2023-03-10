from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import ListView, TemplateView
from .models import Laptop
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

        if category == 'desktops':
            items = Laptop.objects.all()
        elif category == 'laptops':
            items = Laptop.objects.all()

        return items

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.kwargs['category']
        items = self.request.session.get('items')
        if items is not None:
            context['product_codes'] = items[self.kwargs['category']]

        return context


class CartView(TemplateView):
    template_name = 'cart.html'

    def get(self, request, *args, **kwargs):
        products = dict()
        total_price = 0
        context = dict()
        is_cart_empty = True
        items = request.session.get('items')

        if items is not None:
            for category, product_list in items.items():
                if len(product_list) > 0:
                    is_cart_empty = False
                    if category == 'laptops':
                        products['laptops'] = list()
                        for product_code, product_count in product_list.items():
                            item = Laptop.objects.get(product_code=product_code)
                            laptop = (product_count, item)
                            total_price += item.price * product_count
                            products['laptops'].append(laptop)
            context = {
                'products': products,
                'total_price': total_price,
                'is_cart_empty': is_cart_empty
            }

        return render(request, self.template_name, context=context)


class CartAddProductView(TemplateView):
    def post(self, request, *args, **kwargs):
        category = request.POST['category']
        product_code = request.POST['product_code']

        if request.session.get('items') is None:
            request.session['items'] = dict()

        if request.session['items'].get(category, None) is None:
            request.session['items'][category] = dict()

        if request.session['items'][category].get(product_code) is None:
            request.session['items'][category][product_code] = 1
        else:
            request.session['items'][category][product_code] += 1
        request.session.modified = True

        return HttpResponse(status=200)


class CartReduceProductCountView(TemplateView):
    def post(self, request, *args, **kwargs):
        category = request.POST['category']
        product_code = request.POST['product_code']

        if request.session.get('items') is not None:
            if request.session['items'].get(category, None) is not None:
                if request.session['items'][category][product_code] > 1:
                    request.session['items'][category][product_code] -= 1
        request.session.modified = True

        return HttpResponse(product_code)


class CartRemoveProductView(TemplateView):
    def post(self, request, *args, **kwargs):
        category = request.POST['category']
        product_code = request.POST['product_code']

        if request.session.get('items') is not None:
            if request.session['items'].get(category, None) is not None:
                del request.session['items'][category][product_code]
        request.session.modified = True

        return HttpResponse(product_code)
