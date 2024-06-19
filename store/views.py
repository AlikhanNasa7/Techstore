from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string

from .forms import UserRegistrationForm, LoginForm, ApplicationForm

from django.contrib.auth import authenticate, login, logout

from django.http import HttpResponse, JsonResponse, HttpResponseRedirect

from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods

from .models import Product, Cart, CartItem, Brand, ProductAttribute, ProductAttributeValue
from django.core.paginator import Paginator

import pywhatkit as kit
import datetime


def index(request):
    new_products = Product.objects.all().order_by('-date_added')[:5]
    top_products = Product.objects.all().order_by('-purchases')[:5]
    print(new_products)
    print(top_products)
    return render(request, 'index.html', {'new_products': new_products, 'top_products': top_products})


def brands(request, brand_name):
    capitalized_name = brand_name[0].upper() + brand_name[1:]
    brand_products = Product.objects.filter(brand__name=capitalized_name)
    print(brand_products)
    return render(request, 'store/brand_products.html',
                  {'products': brand_products, 'brand_name': capitalized_name})


def search_product(request):
    print(request.method)
    product_search = request.GET.get('search')
    print(product_search)

    search_products = Product.objects.filter(name__icontains=product_search)

    context = {
        'search_products': search_products,
        'search': product_search
    }

    return render(request, 'store/search-products.html', context)


def send_message(request):
    phone_number = request.GET.get('phone_number')
    name = request.GET.get('name')

    now = datetime.datetime.now()
    send_at_hour = now.hour
    send_at_minute = now.minute + 1 if now.second < 50 else now.minute + 2

    message = 'Привет, ' + name
    print(phone_number, name)
    try:
        kit.sendwhatmsg(phone_number, message, send_at_hour, send_at_minute)
        return JsonResponse({"status": "Message scheduled"})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


def about(request):
    return render(request, 'store/about.html')


def sercent(request):
    if request.method == 'POST':
        form = ApplicationForm(request.POST)
        print(form.is_valid())
        print(form.errors)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = ApplicationForm()
    return render(request, 'store/sercent.html', {"form": form})


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


def product_type(request, product_type):
    reformat_type = {
        'processors': 'Processor',
        'ssd-disks': 'SSDdisk',
        'videocards': 'Videocard',
        'motherboards': 'matPLat',
        'power-supplies': 'powerBlock',
        'monitors': 'Monitor',
        'cases': 'corpus',
        'rams': 'ozy',
        'peripherals': 'peref'
    }
    titles = {
        'processors': 'Процессоры',
        'ssd-disks': 'Диски',
        'videocards': 'Видеокарты',
        'motherboards': 'Материнские платы',
        'power-supplies': 'Блоки питания',
        'monitors': 'Мониторы',
        'cases': 'Корпуса',
        'rams': 'ОЗУ',
        'peripherals': 'Периферия'
    }
    short_parameters = {
        'processors': {
            'show_names': ['Тип процессора', 'Сокет', 'Общее количество ядер', 'Количество потоков', 'Тактовая частота',
                           'Микроархитектура'],
            'db_names': ['Тип процессора', 'Сокет', 'Общее количество ядер', 'Количество потоков', 'Тактовая частота',
                         'Микроархитектура']
        },
        'ssd-disks': 'Диски',
        'videocards': 'Видеокарты',
        'motherboards': 'Материнские платы',
        'power-supplies': 'Блоки питания',
        'monitors': 'Мониторы',
        'cases': 'Корпуса',
        'rams': 'ОЗУ',
        'peripherals': 'Периферия'
    }

    title = titles[product_type]
    parameters = short_parameters[product_type]

    products = Product.objects.filter(product_type__name=reformat_type[product_type])

    if len(request.GET.keys()):
        query_param = list(request.GET.keys())[0]
        print(
            query_param
        )

        if query_param == 'made_by':
            products = products.filter(brand__name=request.GET.get(query_param))
        if query_param == 'processor_type':
            print(request.GET.get(query_param))
            products = products.filter(name__icontains=request.GET.get(query_param))

        if query_param == 'core_quantity':
            processor_type_attribute = ProductAttribute.objects.get(name='Общее количество ядер')

            # Then, find all ProductAttributeValue instances with this attribute and value 'Ryzen 3'
            processor_type_values = ProductAttributeValue.objects.filter(
                attribute=processor_type_attribute,
                value=request.GET.get(query_param)
            )
            print(processor_type_values)

            products = Product.objects.filter(product_values__in=processor_type_values).distinct()

            print(products)

        if query_param == 'storage_capacity':
            processor_type_attribute = ProductAttribute.objects.get(name='Объем накопителя')

            # Then, find all ProductAttributeValue instances with this attribute and value 'Ryzen 3'
            processor_type_values = ProductAttributeValue.objects.filter(
                attribute=processor_type_attribute,
                value=request.GET.get(query_param)
            )
            print(processor_type_values)

            products = Product.objects.filter(product_values__in=processor_type_values).distinct()

        if query_param == 'has_dram':
            processor_type_attribute = ProductAttribute.objects.get(name='DRAM буфер')

            processor_type_values = ProductAttributeValue.objects.filter(
                attribute=processor_type_attribute,
                value=request.GET.get(query_param)
            )
            print(processor_type_values)

            products = Product.objects.filter(product_values__in=processor_type_values).distinct()

        if query_param == 'graphic_processor_made_by':
            processor_type_attribute = ProductAttribute.objects.get(name='Производители графического процессора')

            processor_type_values = ProductAttributeValue.objects.filter(
                attribute=processor_type_attribute,
                value=request.GET.get(query_param)
            )
            print(processor_type_values)

            products = Product.objects.filter(product_values__in=processor_type_values).distinct()

        if query_param == 'graphic_processor':
            processor_type_attribute = ProductAttribute.objects.get(name='Графический процессор')

            processor_type_values = ProductAttributeValue.objects.filter(
                attribute=processor_type_attribute,
                value=request.GET.get(query_param)
            )
            print(processor_type_values)

            products = Product.objects.filter(product_values__in=processor_type_values).distinct()

        if query_param == 'socket':
            processor_type_attribute = ProductAttribute.objects.get(name='Сокет', product_type__name='matPLat')

            processor_type_values = ProductAttributeValue.objects.filter(
                attribute=processor_type_attribute,
                value=request.GET.get(query_param)
            )
            print(processor_type_values)

            products = Product.objects.filter(product_values__in=processor_type_values).distinct()

        if query_param == 'memory_type':
            processor_type_attribute = ProductAttribute.objects.get(name='Тип поддерживаемой памяти')

            processor_type_values = ProductAttributeValue.objects.filter(
                attribute=processor_type_attribute,
                value=request.GET.get(query_param)
            )
            print(processor_type_values)

            products = Product.objects.filter(product_values__in=processor_type_values).distinct()
        #have to be fixed
        #
        #
        #
        #
        if query_param == 'power-supply_power':
            processor_type_attribute = ProductAttribute.objects.get(name='Мощность (номинал)')

            processor_type_values = ProductAttributeValue.objects.filter(
                attribute=processor_type_attribute,
                value=request.GET.get(query_param)
            )
            print(processor_type_values)

            products = Product.objects.filter(product_values__in=processor_type_values).distinct()

        if query_param == 'form-factor':
            processor_type_attribute = ProductAttribute.objects.get(name='Форм-фактор')

            processor_type_values = ProductAttributeValue.objects.filter(
                attribute=processor_type_attribute,
                value=request.GET.get(query_param)
            )
            print(processor_type_values)

            products = Product.objects.filter(product_values__in=processor_type_values).distinct()


    paginator = Paginator(products, 5)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    current_page = page_obj.number
    total_pages = paginator.num_pages

    start_page = max(current_page - 1, 1)
    end_page = min(current_page + 1, total_pages)

    page_range = range(start_page, end_page + 1)

    brands = Product.objects.filter(product_type__name=reformat_type[product_type])

    return render(request, 'store/products_by_type.html',
                  {'page_obj': page_obj, 'page_range': page_range, 'title': title, 'parameters': parameters,
                   'product_type': product_type})


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
