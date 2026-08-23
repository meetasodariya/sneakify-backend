import uuid
from django.db import models
from django.conf import settings
from apps.sneakers.models import SneakerModel

class CustomDesign(models.Model):
    """Stores full 3D customizer configuration and 3D canvas snapshot."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='custom_designs'
    )
    base_model = models.ForeignKey(
        SneakerModel,
        on_delete=models.CASCADE,
        related_name='customizations'
    )
    title = models.CharField(max_length=150, default="Custom Sneaker")
    
    # 3D Part configuration json (Valtio store dump)
    # { "parts": { "upper": { "color": "#111827", "material": "leather" }, ... }, "text": { "content": "SNEAK", "position": "heel" } }
    configuration = models.JSONField(
        help_text="Full 3D part configuration (colors, materials, finishes, custom text)"
    )
    
    # Snapshot image URL (rendered directly on 3D canvas and saved to Cloudinary / data URL)
    preview_image_url = models.URLField(max_length=1000, blank=True)
    
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=11995.00)
    is_public = models.BooleanField(default=True, help_text="Showcase in community feed")
    likes_count = models.PositiveIntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} ({self.id})"
