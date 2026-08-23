from django.contrib import admin
from .models import Category, SneakerModel, SneakerSize, ProductImage

class SneakerSizeInline(admin.TabularInline):
    model = SneakerSize
    extra = 4

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 3

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(SneakerModel)
class SneakerModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'sku', 'category', 'gender', 'base_price', 'is_customizable', 'is_bestseller', 'is_featured')
    list_filter = ('category', 'gender', 'is_customizable', 'is_bestseller', 'is_featured')
    search_fields = ('name', 'sku', 'description')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [SneakerSizeInline, ProductImageInline]
