from django.shortcuts import render
from account.forms import UserLoginForm, UserRegistrationForm
from django.contrib import auth


# Create your views here.

def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = auth.authenticate(username=username, password=password)
            if user is not None:
                auth.login(request, user)
                return render(request, '')

    form = UserLoginForm()
    context = {'form': form}

    return render(request, 'store/login.html', context)


def user_logout(request):
    pass


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'store')
    else:
        form = UserRegistrationForm()

    context = {'form': form}

    return render(request, 'store/account/reg.html')

