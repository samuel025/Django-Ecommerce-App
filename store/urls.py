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
from core.views import Contact, HomeView, ItemDetailView, Pay_on_delivery, ShopView, add_to_cart, ItemDetailView, Cart, remove_from_cart, remove_single_item_from_cart, CheckoutView, final_checkout, PaymentView, Payment_on_delivery
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
    path('verify/<int:id>', PaymentView.as_view(), name='verify_payment'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('on_delivery', Pay_on_delivery, name='on_delivery'),
    path('product/<slug>/', ItemDetailView, name='product_page'),
    path('pay_on_delivery', Payment_on_delivery, name='payment_on_delivery'),
    path('final-checkout/', final_checkout, name='f_checkout'),
    path('accounts/', include('allauth.urls')),
    path('api/', include('rest_api.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)