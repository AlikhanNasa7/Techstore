from django.shortcuts import render, redirect, get_object_or_404
from .forms import UserRegistrationForm, LoginForm

from django.contrib.auth import authenticate, login, logout

from django.http import HttpResponse, JsonResponse

from django.contrib.auth.decorators import login_required

from .models import Product, Cart, CartItem
from django.core.paginator import Paginator

def index(request):
    products = Product.objects.all()
    return render(request, 'index.html', {'products': products})


def about(request):
    return render(request, 'store/about.html')


def sercent(request):
    return render(request, 'store/sercent.html')


def shipping(request):
    return render(request, 'store/shipping.html')


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)

        if form.is_valid():
            cd = form.cleaned_data

            new_user = form.save(commit=False)
            print(new_user)

            new_user.set_password(cd['password'])

            new_user.save()

            return render(request, '../account/templates/templates/store/account/register_done.html', {'form': form})
    else:
        form = UserRegistrationForm()

    return render(request, '../account/templates/templates/store/account/register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            cd = form.cleaned_data
            username = cd['username']
            password = cd['password']

            user = authenticate(username=username, password=password)

            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse('Logged in successfully')
                else:
                    return HttpResponse('Your account is disabled')
            else:
                return HttpResponse('Invalid login details')
    else:
        form = LoginForm()

    return render(request, '../account/templates/templates/store/account/login.html', {'form': form})


@login_required
def add_to_cart(request, product_id):
    product = Product.objects.get(id=product_id)

    try:
        cart = Cart.objects.get(user=request.user)
    except Cart.DoesNotExist:
        cart = Cart.objects.create(user=request.user)

    try:
        cart_item = CartItem.objects.get(cart=cart, product=product)
        cart_item.quantity += 1
        cart_item.save()
    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(cart=cart, product=product, quantity=1)

    return JsonResponse({'status': 'success', 'message': 'CartItem has been added to your cart'})


@login_required
def remove_from_cart(request, product_id):
    cart = get_object_or_404(Cart, user=request.user)
    cart_item = get_object_or_404(CartItem, cart=cart, product=product_id)
    cart_item.delete()

    return JsonResponse({'status': 'success', 'message': 'CartItem has been deleted from your cart'})


def processors(request):
    products = Product.objects.filter(product_type__name='Processor')
    paginator = Paginator(products, 2)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    current_page = page_obj.number
    total_pages = paginator.num_pages

    start_page = max(current_page - 1, 1)
    end_page = min(current_page + 1, total_pages)

    page_range = range(start_page, end_page + 1)
    return render(request, 'store/processors.html', {'page_obj': page_obj, 'page_range': page_range})


def product(request, product_id):
    user = request.user
    is_in_cart = False
    product = get_object_or_404(Product, id=product_id)
    if user is not None and user.is_authenticated:
        user_cart = user.cart
        cart_items = user_cart.items
        if cart_items.filter(product=product).exists():
            is_in_cart = True

    curr_product = Product.objects.get(id=product.id)
    print(curr_product)
    return render(request, 'store/product.html', {'product': curr_product, 'is_in_cart': is_in_cart})


def ssd_disks(request):
    products = Product.objects.filter(product_type__name='Processor')
    return render(request, 'store/ssd_disks.html', {'processors': products})


def video_carts(request):
    products = Product.objects.filter(product_type__name='Processor')
    return render(request, 'store/processors.html', {'processors': products})


def motherboards(request):
    products = Product.objects.filter(product_type__name='SSD Disk')
    return render(request, 'store/processors.html', {'processors': products})


def power_supplies(request):
    products = Product.objects.filter(product_type__name='Power Supply')
    return render(request, 'store/processors.html', {'processors': products})


def monitors(request):
    products = Product.objects.filter(product_type__name='Monitor')
    return render(request, 'store/processors.html', {'processors': products})


def cases(request):
    products = Product.objects.filter(product_type__name='Case')
    return render(request, 'store/processors.html', {'processors': products})


def rams(request):
    products = Product.objects.filter(product_type__name='RAM')
    return render(request, 'store/processors.html', {'processors': products})


def peripherals(request):
    products = Product.objects.filter(product_type__name='Peripheral')
    return render(request, 'store/processors.html', {'processors': products})


