from django.urls import path, include
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

from Techstore import settings
from . import views
urlpatterns = [
    path('', views.index, name='index'),
    path('processors/', views.processors, name='processors'),
    path('product/<int:product_id>/', views.product, name='product'),
    path('ssd-disks/', views.ssd_disks, name='ssd-disks'),
    path('video-carts/', views.video_carts, name='video-carts'),
    path('motherboards/', views.motherboards, name='motherboards'),
    path('power-supplies/', views.power_supplies, name='power-supplies'),
    path('monitors/', views.monitors, name='monitors'),
    path('cases/', views.cases, name='cases'),
    path('rams/', views.rams, name='rams'),
    path('peripherals/', views.peripherals, name='peripherals'),
    path('about/', views.about, name='about'),
    path('shipping/', views.shipping, name='shipping'),
    path('sercent/', views.sercent, name='sercent'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)