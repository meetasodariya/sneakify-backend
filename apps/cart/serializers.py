from rest_framework import serializers
from .models import Cart, CartItem
from apps.sneakers.serializers import SneakerListSerializer
from apps.customizer.serializers import CustomDesignSerializer

class CartItemSerializer(serializers.ModelSerializer):
    sneaker_detail = SneakerListSerializer(source='sneaker', read_only=True)
    custom_design_detail = CustomDesignSerializer(source='custom_design', read_only=True)
    item_name = serializers.CharField(read_only=True)
    preview_image = serializers.CharField(read_only=True)
    total_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = CartItem
        fields = [
            'id',
            'cart',
            'sneaker',
            'sneaker_detail',
            'custom_design',
            'custom_design_detail',
            'item_name',
            'preview_image',
            'size',
            'quantity',
            'unit_price',
            'total_price',
            'created_at',
        ]
        read_only_fields = ['id', 'cart', 'created_at']

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total_items = serializers.IntegerField(read_only=True)
    subtotal = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = Cart
        fields = [
            'id',
            'items',
            'total_items',
            'subtotal',
            'created_at',
            'updated_at',
        ]
