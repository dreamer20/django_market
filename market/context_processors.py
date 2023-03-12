from .models import Category


def category_list(request):
    categories = Category.objects.all()
    return {'category_list': categories}


def items_count(request):
    items_count = request.session.get('items_count')

    if items_count is None:
        items_count = 0

    return {'items_count': items_count}
