from .models import Category


def category_list(request):
    categories = Category.objects.all()
    return {'category_list': categories}
