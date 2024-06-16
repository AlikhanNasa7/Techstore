from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from store.models import Product, Cart, CartItem, Favourites, FavouriteItem, Order, OrderItem
from django.contrib import messages
from django.http.response import HttpResponse, JsonResponse, HttpResponseRedirect
from django.core.paginator import Paginator
from .forms import OrderForm
import stripe
from django.conf import settings
from django.urls import reverse, reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from http import HTTPStatus

stripe.api_key = settings.STRIPE_SECRET_KEY


@login_required(login_url='account:user-login')
@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)

    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        cart_item.quantity += 1
    cart_item.save()

    messages.success(request, f'Added {product.name} to your cart.')
    return redirect('cart:cart_detail')


@login_required(login_url='account:user-login')
def add_to_favourites(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    favourites, created = Favourites.objects.get_or_create(user=request.user)
    favourite_item, created = FavouriteItem.objects.get_or_create(favourites_list=favourites, product=product)
    if created:
        messages.success(request, f'Added {product.name} to your favourites.')
    else:
        messages.info(request, f'{product.name} is already in your favourites.')
    return redirect('cart:favourites_detail')


@login_required(login_url='account:user-login')
def decrease_from_cart(request, product_id):
    cart = get_object_or_404(Cart, user=request.user)
    cart_item = get_object_or_404(CartItem, cart=cart, product_id=product_id)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
        messages.success(request, f'Reduced quantity of {cart_item.product.name} in your cart.')
    else:
        cart_item.delete()
        messages.success(request, f'Removed {cart_item.product.name} from your cart.')
    return redirect('cart:cart_detail')


def remove_from_cart(request, product_id):
    user_cart = get_object_or_404(Cart, user=request.user)
    product = get_object_or_404(Product, id=product_id)

    cart_item = get_object_or_404(CartItem, cart=user_cart, product=product)
    if cart_item:
        cart_item.delete()

    return redirect('cart:cart_detail')


@login_required(login_url='account:user-login')
def remove_from_favourites(request, product_id):
    user_favourites = get_object_or_404(Favourites, user=request.user)
    favourite_item = get_object_or_404(FavouriteItem, favourites_list=user_favourites, product_id=product_id)
    favourite_item.delete()
    messages.success(request, f'Removed {favourite_item.product.name} from your favourites.')
    return redirect('cart:favourites_detail')


@login_required(login_url='account:user-login')
def cart(request):
    user_cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = user_cart.items.all()
    paginator = Paginator(cart_items, 5)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    current_page = page_obj.number
    total_pages = paginator.num_pages

    start_page = max(current_page - 1, 1)
    end_page = min(current_page + 1, total_pages)

    page_range = range(start_page, end_page + 1)

    total_price = sum(item.get_total_price() for item in cart_items)
    return render(request, 'store/cart.html',
                  {'cart_items': cart_items, 'total_price': total_price, 'page_obj': page_obj,
                   'page_range': page_range})


@login_required(login_url='account:user-login')
def favourites(request):
    print(request.user)
    user_favourites, created = Favourites.objects.get_or_create(user=request.user)
    favourite_items = user_favourites.items.all()
    return render(request, 'store/favourites.html', {'favourite_items': favourite_items})


@login_required(login_url='account:user-login')
@csrf_exempt
def booking(request):
    user_cart = Cart.objects.get(user=request.user)
    cart_items = user_cart.items.all()

    total_price = sum(item.get_total_price() for item in cart_items)

    if request.method == 'POST':
        print(request.POST)
        form = OrderForm(request.POST)
        print(form.is_valid())
        print(form.errors)
        if form.is_valid():
            name = form.cleaned_data['name']
            address = form.cleaned_data['address']
            phone_number = form.cleaned_data['phone_number']

            delivery_option = form.cleaned_data['delivery_option']
            payment_option = form.cleaned_data['payment_option']
            total_price = form.cleaned_data['total_price']

            order_instance = Order(user=request.user, name=name, address=address, phone_number=phone_number,
                                   payment_option=payment_option, delivery_option=delivery_option,
                                   total_price=total_price)

            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[
                    {
                        # Provide the exact Price ID (for example, pr_1234) of the product you want to sell
                        'price': 'price_1PQsnY09YDBQc1tNaSHSWLzL',
                        'quantity': 1,
                    },
                ],
                mode='payment',
                success_url=settings.DOMAIN_URL + reverse('cart:order_success'),
                cancel_url=settings.DOMAIN_URL + '/cancel.html',
            )

            order_instance.save()

            for cart_item in user_cart:
                order_item = OrderItem.objects.create(order=order_instance, product=cart_item.product,
                                                      quantity=cart_item.quantity,
                                                      price=cart_item.product.price * cart_item.quantity)
                order_item.save()

            return HttpResponseRedirect(checkout_session.url, status=HTTPStatus.SEE_OTHER)
    else:
        form = OrderForm()

    return render(request, 'store/booking.html', {'total_price': total_price, 'form': form})


def order_success(request):
    return render(request, 'store/order-success.html')


def orders(request):
    user = request.user
    user_orders = user.orders.all()
    return render(request, 'store/orders.html', {'user': user, 'user_orders': user_orders})


def order(request, order_id):
    curr_order = get_object_or_404(Order, id=order_id)
    return render(request, 'store/order.html', {'order': curr_order})
