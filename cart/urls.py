from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add-to-cart'),
    path('add-to-favourites/<int:product_id>/', views.add_to_favourites, name='add-to-favourites'),
    path('decrease-from-cart/<int:product_id>/', views.decrease_from_cart, name='cart-decrease'),
    path('remove-from-favourites/<int:product_id>/', views.remove_from_favourites, name='favourites-remove'),
    path('remove-from-cart/<int:product_id>/', views.remove_from_cart, name='cart-remove'),
    path('cart/', views.cart, name='cart_detail'),
    path('favourites/', views.favourites, name='favourites_detail'),
    path('booking/', views.booking, name='booking'),
    path('order-success/', views.order_success, name='order_success'),
    path('orders/', views.orders, name='orders'),
    path('order/<int:order_id>/', views.order, name='order_detail'),
]
