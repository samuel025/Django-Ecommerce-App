"""store URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from pytest import Item
from core.views import Contact, HomeView, ItemDetailView, ShopView, add_to_cart, ItemDetailView, Cart, remove_from_cart, remove_single_item_from_cart, CheckoutView
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomeView.as_view(), name='home_page'),
    path('remove-from-cart/<slug>', remove_from_cart, name='remove-from-cart'),
    path('shop/', ShopView.as_view(), name='shop_view'),
    path('remove-single-item-from-cart/<slug>', remove_single_item_from_cart, name='remove_single_item_from_cart'),
    path('add-to-cart/<slug>', add_to_cart, name='add-to-cart'),
    path('cart/', Cart.as_view(), name='cart'),
    path('contact/', Contact.as_view(), name='contact'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('product/<slug>/', ItemDetailView.as_view(), name='product_page'),
    path('accounts/', include('allauth.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)