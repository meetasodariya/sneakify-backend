from django.urls import path
from .views import (
    SneakerReviewsListView,
    WishlistView,
    ToggleWishlistView,
)

app_name = 'reviews'

urlpatterns = [
    path('sneakers/<uuid:sneaker_id>/', SneakerReviewsListView.as_view(), name='sneaker_reviews'),
    path('wishlist/', WishlistView.as_view(), name='wishlist_list'),
    path('wishlist/toggle/', ToggleWishlistView.as_view(), name='wishlist_toggle'),
]
