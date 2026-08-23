from rest_framework import serializers
from .models import Category, SneakerModel, SneakerSize, ProductImage

class CategorySerializer(serializers.ModelSerializer):
    sneaker_count = serializers.IntegerField(source='sneakers.count', read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description', 'image_url', 'sneaker_count']

class SneakerSizeSerializer(serializers.ModelSerializer):
    is_available = serializers.SerializerMethodField()

    class Meta:
        model = SneakerSize
        fields = ['id', 'size_uk', 'stock_quantity', 'is_available']

    def get_is_available(self, obj):
        return obj.stock_quantity > 0

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image_url', 'angle_label', 'is_primary', 'order']

class SneakerListSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    primary_image = serializers.SerializerMethodField()

    class Meta:
        model = SneakerModel
        fields = [
            'id',
            'name',
            'slug',
            'sku',
            'category_name',
            'gender',
            'base_price',
            'original_price',
            'is_customizable',
            'is_bestseller',
            'is_featured',
            'is_new_release',
            'rating',
            'review_count',
            'primary_image',
        ]

    def get_primary_image(self, obj):
        primary = obj.images.filter(is_primary=True).first()
        if primary:
            return primary.image_url
        first = obj.images.first()
        return first.image_url if first else None

class SneakerDetailSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    sizes = SneakerSizeSerializer(many=True, read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)

    class Meta:
        model = SneakerModel
        fields = [
            'id',
            'name',
            'slug',
            'sku',
            'category',
            'gender',
            'base_price',
            'original_price',
            'description',
            'details',
            'is_customizable',
            'is_bestseller',
            'is_featured',
            'is_new_release',
            'model_3d_url',
            'rating',
            'review_count',
            'sizes',
            'images',
            'created_at',
        ]
