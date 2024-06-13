from django.shortcuts import render
from account.forms import UserLoginForm, UserRegistrationForm
from django.contrib import auth
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse


# Create your views here.

def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        print(form.errors)
        if form.is_valid():

            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = auth.authenticate(username=username, password=password)
            if user is not None:
                auth.login(request, user)
                return HttpResponseRedirect(reverse('index'))
    else:
        form = UserLoginForm()
    context = {'form': form}

    return render(request, 'store/login.html', context)


def user_logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('index'))


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('index'))
    else:
        form = UserRegistrationForm()

    context = {'form': form}

    return render(request, 'store/account/reg.html', context)


def profile(request):
    return render(request, 'store/profile.html')
