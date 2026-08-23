import uuid
from django.db import models
from django.conf import settings
from apps.sneakers.models import SneakerModel
from apps.customizer.models import CustomDesign

class Cart(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='cart'
    )
    session_key = models.CharField(max_length=100, blank=True, null=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        if self.user:
            return f"Cart of {self.user.email}"
        return f"Guest Cart ({self.session_key})"

    @property
    def total_items(self):
        return sum(item.quantity for item in self.items.all())

    @property
    def subtotal(self):
        return sum(item.total_price for item in self.items.all())

class CartItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    
    # Either a standard catalog sneaker or a customized 3D design
    sneaker = models.ForeignKey(SneakerModel, on_delete=models.CASCADE, null=True, blank=True)
    custom_design = models.ForeignKey(CustomDesign, on_delete=models.CASCADE, null=True, blank=True)
    
    size = models.CharField(max_length=10, default="UK 9")
    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def total_price(self):
        return self.unit_price * self.quantity

    @property
    def item_name(self):
        if self.custom_design:
            return self.custom_design.title
        return self.sneaker.name if self.sneaker else "Sneaker"

    @property
    def preview_image(self):
        if self.custom_design and self.custom_design.preview_image_url:
            return self.custom_design.preview_image_url
        if self.sneaker:
            primary = self.sneaker.images.filter(is_primary=True).first()
            if primary:
                return primary.image_url
            first = self.sneaker.images.first()
            return first.image_url if first else None
        return ""

    def __str__(self):
        return f"{self.quantity}x {self.item_name} ({self.size})"
