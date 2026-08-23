import uuid
import random
from django.db import models
from django.conf import settings
from apps.sneakers.models import SneakerModel
from apps.customizer.models import CustomDesign

def generate_order_number():
    return f"SNK-{random.randint(100000, 999999)}"

def generate_tracking_number():
    return f"TRK{random.randint(10000000, 99999999)}IN"

class Order(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending Payment'),
        ('handcrafting', 'Custom Handcrafting in Progress'),
        ('quality_check', 'Studio Quality Check'),
        ('shipped', 'Shipped with Courier'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order_number = models.CharField(max_length=30, unique=True, default=generate_order_number, db_index=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='orders'
    )
    
    # Shipping Information
    customer_name = models.CharField(max_length=200)
    customer_email = models.EmailField()
    customer_phone = models.CharField(max_length=20)
    shipping_address_line1 = models.CharField(max_length=255)
    shipping_address_line2 = models.CharField(max_length=255, blank=True)
    shipping_city = models.CharField(max_length=100)
    shipping_state = models.CharField(max_length=100)
    shipping_postal_code = models.CharField(max_length=20)
    shipping_country = models.CharField(max_length=100, default='India')

    # Status & Logistics
    status = models.CharField(max_length=25, choices=STATUS_CHOICES, default='pending')
    tracking_number = models.CharField(max_length=50, unique=True, default=generate_tracking_number)
    courier_partner = models.CharField(max_length=100, default="Bluedart Express")
    estimated_delivery = models.CharField(max_length=100, default="5-7 Business Days")
    
    # Financials
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    tax_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    shipping_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.order_number} ({self.customer_name}) - {self.status}"

class OrderItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    
    sneaker = models.ForeignKey(SneakerModel, on_delete=models.SET_NULL, null=True, blank=True)
    custom_design = models.ForeignKey(CustomDesign, on_delete=models.SET_NULL, null=True, blank=True)
    
    # Immutable snapshot of customizer design configuration at time of purchase
    design_snapshot = models.JSONField(null=True, blank=True)
    
    item_title = models.CharField(max_length=200)
    preview_image_url = models.URLField(max_length=1000, blank=True)
    size = models.CharField(max_length=10)
    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity}x {self.item_title} ({self.size})"
