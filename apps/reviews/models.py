import uuid
from django.db import models
from django.conf import settings
from apps.sneakers.models import SneakerModel
from apps.customizer.models import CustomDesign

class Review(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reviews')
    sneaker = models.ForeignKey(SneakerModel, on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveSmallIntegerField(default=5) # 1 to 5
    title = models.CharField(max_length=150)
    comment = models.TextField()
    is_verified_buyer = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        unique_together = ('user', 'sneaker')

    def __str__(self):
        return f"{self.rating}★ by {self.user.email} on {self.sneaker.name}"

class WishlistItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='wishlist')
    sneaker = models.ForeignKey(SneakerModel, on_delete=models.CASCADE, null=True, blank=True)
    custom_design = models.ForeignKey(CustomDesign, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Wishlist item of {self.user.email}"
