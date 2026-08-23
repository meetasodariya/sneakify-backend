from rest_framework import serializers
from .models import CustomDesign
from apps.sneakers.serializers import SneakerListSerializer

class CustomDesignSerializer(serializers.ModelSerializer):
    creator_name = serializers.SerializerMethodField()
    base_model_name = serializers.CharField(source='base_model.name', read_only=True)

    class Meta:
        model = CustomDesign
        fields = [
            'id',
            'user',
            'creator_name',
            'base_model',
            'base_model_name',
            'title',
            'configuration',
            'preview_image_url',
            'total_price',
            'is_public',
            'likes_count',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'user', 'likes_count', 'created_at', 'updated_at']

    def get_creator_name(self, obj):
        if obj.user:
            return obj.user.full_name or obj.user.username
        return "Sneakify Creator"

class CustomDesignDetailSerializer(serializers.ModelSerializer):
    base_model = SneakerListSerializer(read_only=True)
    creator_name = serializers.SerializerMethodField()

    class Meta:
        model = CustomDesign
        fields = [
            'id',
            'user',
            'creator_name',
            'base_model',
            'title',
            'configuration',
            'preview_image_url',
            'total_price',
            'is_public',
            'likes_count',
            'created_at',
        ]

    def get_creator_name(self, obj):
        if obj.user:
            return obj.user.full_name or obj.user.username
        return "Sneakify Creator"
