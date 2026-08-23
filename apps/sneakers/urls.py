from django.urls import path
from .views import (
    CategoryListView,
    SneakerListView,
    SneakerDetailView,
    BestsellersView,
    FeaturedSneakersView,
)

app_name = 'sneakers'

urlpatterns = [
    path('categories/', CategoryListView.as_view(), name='category_list'),
    path('bestsellers/', BestsellersView.as_view(), name='bestsellers'),
    path('featured/', FeaturedSneakersView.as_view(), name='featured'),
    path('', SneakerListView.as_view(), name='sneaker_list'),
    path('<slug:slug>/', SneakerDetailView.as_view(), name='sneaker_detail'),
]
