from django.urls import path
from . import views


urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('category/<str:category>', views.CategoryView.as_view(), name='category'),
    path('category/<str:category>/<str:product_code>/', views.ProdcutDetailView.as_view(), name='product_detail'),
    path('cart/', views.CartView.as_view(), name='cart'),
    path('cart/remove/', views.CartRemoveProductView.as_view(), name='cart_remove'),
    path('cart/add/', views.CartAddProductView.as_view(), name='cart_add'),
    path('cart/reduce/', views.CartReduceProductCountView.as_view(), name='cart_reduce'),
    path('cart/order/success/', views.OrderSuccessView.as_view(), name='order_success'),
    path('cart/order/', views.OrderView.as_view(), name='order'),
]
