from django.contrib import admin
from .models import Review, WishlistItem

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'sneaker', 'rating', 'title', 'is_verified_buyer', 'created_at')
    list_filter = ('rating', 'is_verified_buyer', 'created_at')
    search_fields = ('user__email', 'sneaker__name', 'title', 'comment')

@admin.register(WishlistItem)
class WishlistItemAdmin(admin.ModelAdmin):
    list_display = ('user', 'sneaker', 'custom_design', 'created_at')
    list_filter = ('created_at',)
