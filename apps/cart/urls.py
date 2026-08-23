from django.urls import path
from .views import (
    CartView,
    AddToCartView,
    UpdateCartItemView,
    ClearCartView,
)

app_name = 'cart'

urlpatterns = [
    path('', CartView.as_view(), name='cart_detail'),
    path('add/', AddToCartView.as_view(), name='cart_add'),
    path('items/<uuid:item_id>/', UpdateCartItemView.as_view(), name='cart_item_update'),
    path('clear/', ClearCartView.as_view(), name='cart_clear'),
]
