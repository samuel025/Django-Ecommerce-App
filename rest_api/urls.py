from django.urls import include, path
from .views import ItemListView, AddToCartView, CartAPIView, ItemDetailAPIView

urlpatterns = [
    path('', ItemListView.as_view()),
    path('add_to_cart/<slug:slug>', AddToCartView.as_view()),
    path('cart/', CartAPIView.as_view()),
    path('item/<slug:slug>', ItemDetailAPIView.as_view()),
    path('auth/', include('dj_rest_auth.urls')),  # Handles login, logout
    path('auth/registration/', include('dj_rest_auth.registration.urls')),

]