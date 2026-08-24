from django.contrib import admin
from .models import CustomDesign

@admin.register(CustomDesign)
class CustomDesignAdmin(admin.ModelAdmin):
    list_display = ('title', 'id', 'base_model', 'user', 'total_price', 'is_public', 'likes_count', 'created_at')
    list_filter = ('is_public', 'base_model', 'created_at')
    search_fields = ('title', 'user__email')
