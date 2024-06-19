from django.urls import path, include
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

from Techstore import settings
from . import views
urlpatterns = [
    path('', views.index, name='index'),
    path('product/<int:product_id>/', views.product, name='product'),
    path('search-product', views.search_product, name='search_product'),
    #
    path('about/', views.about, name='about'),
    path('shipping/', views.shipping, name='shipping'),
    path('sercent/', views.sercent, name='sercent'),
    #
    path('<str:product_type>/', views.product_type, name='product_type'),
    path('brand/<str:brand_name>/', views.brands, name='brands'),
    path('send-message', views.send_message, name='send_message'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)