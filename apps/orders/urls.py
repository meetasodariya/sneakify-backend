from django.urls import path
from .views import (
    CreateOrderFromCartView,
    UserOrdersListView,
    OrderDetailView,
    TrackOrderView,
)

app_name = 'orders'

urlpatterns = [
    path('checkout/', CreateOrderFromCartView.as_view(), name='order_checkout'),
    path('my-orders/', UserOrdersListView.as_view(), name='user_orders'),
    path('track/<str:identifier>/', TrackOrderView.as_view(), name='order_track'),
    path('<str:order_number>/', OrderDetailView.as_view(), name='order_detail'),
]
