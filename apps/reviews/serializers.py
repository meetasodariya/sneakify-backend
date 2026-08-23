from rest_framework import serializers
from .models import Review, WishlistItem
from apps.sneakers.serializers import SneakerListSerializer
from apps.customizer.serializers import CustomDesignSerializer

class ReviewSerializer(serializers.ModelSerializer):
    user_name = serializers.SerializerMethodField()

    class Meta:
        model = Review
        fields = [
            'id',
            'user',
            'user_name',
            'sneaker',
            'rating',
            'title',
            'comment',
            'is_verified_buyer',
            'created_at',
        ]
        read_only_fields = ['id', 'user', 'is_verified_buyer', 'created_at']

    def get_user_name(self, obj):
        return obj.user.full_name or obj.user.username

class WishlistItemSerializer(serializers.ModelSerializer):
    sneaker_detail = SneakerListSerializer(source='sneaker', read_only=True)
    custom_design_detail = CustomDesignSerializer(source='custom_design', read_only=True)

    class Meta:
        model = WishlistItem
        fields = [
            'id',
            'sneaker',
            'sneaker_detail',
            'custom_design',
            'custom_design_detail',
            'created_at',
        ]
        read_only_fields = ['id', 'created_at']
