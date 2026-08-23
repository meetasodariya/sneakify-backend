from rest_framework import generics, filters, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Q
from .models import Category, SneakerModel
from .serializers import (
    CategorySerializer,
    SneakerListSerializer,
    SneakerDetailSerializer,
)

class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]

class SneakerListView(generics.ListAPIView):
    serializer_class = SneakerListSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description', 'category__name', 'sku']
    ordering_fields = ['base_price', 'rating', 'created_at']

    def get_queryset(self):
        queryset = SneakerModel.objects.all().prefetch_related('images', 'category')
        
        # Category filter
        category_slug = self.request.query_params.get('category')
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)

        # Gender filter
        gender = self.request.query_params.get('gender')
        if gender:
            queryset = queryset.filter(gender=gender)

        # Price range filter
        min_price = self.request.query_params.get('min_price')
        max_price = self.request.query_params.get('max_price')
        if min_price:
            queryset = queryset.filter(base_price__gte=min_price)
        if max_price:
            queryset = queryset.filter(base_price__lte=max_price)

        # Flags
        is_customizable = self.request.query_params.get('customizable')
        if is_customizable is not None:
            queryset = queryset.filter(is_customizable=is_customizable.lower() == 'true')

        return queryset

class SneakerDetailView(generics.RetrieveAPIView):
    queryset = SneakerModel.objects.all().prefetch_related('sizes', 'images', 'category')
    serializer_class = SneakerDetailSerializer
    lookup_field = 'slug'
    permission_classes = [permissions.AllowAny]

class BestsellersView(generics.ListAPIView):
    serializer_class = SneakerListSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        return SneakerModel.objects.filter(is_bestseller=True).prefetch_related('images', 'category')[:8]

class FeaturedSneakersView(generics.ListAPIView):
    serializer_class = SneakerListSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        return SneakerModel.objects.filter(is_featured=True).prefetch_related('images', 'category')[:6]
