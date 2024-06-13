from django.urls import path
from . import views

app_name = 'account'

urlpatterns = [
    path('login/', views.user_login, name='user-login'),
    path('logout/', views.user_logout, name='user-logout'),
    path('register/', views.register, name='register'),
    path('logout/', views.user_logout, name='user-logout'),
    path('profile/', views.profile, name='profile'),
]