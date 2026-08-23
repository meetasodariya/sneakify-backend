from django.contrib import admin
from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('item_title', 'size', 'quantity', 'unit_price', 'total_price', 'preview_image_url')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'customer_name', 'status', 'total_amount', 'tracking_number', 'created_at')
    list_filter = ('status', 'courier_partner', 'created_at')
    search_fields = ('order_number', 'customer_name', 'customer_email', 'tracking_number')
    inlines = [OrderItemInline]
