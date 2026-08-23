import uuid
from django.db import models
from django.utils.text import slugify

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True, blank=True)
    description = models.TextField(blank=True)
    image_url = models.URLField(max_length=500, blank=True)

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class SneakerModel(models.Model):
    GENDER_CHOICES = (
        ('men', 'Men'),
        ('women', 'Women'),
        ('unisex', 'Unisex'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    sku = models.CharField(max_length=50, unique=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='sneakers')
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='unisex')
    base_price = models.DecimalField(max_digits=10, decimal_places=2)
    original_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    description = models.TextField()
    details = models.JSONField(default=list, blank=True, help_text="List of feature bullet points")
    
    # Flags
    is_customizable = models.BooleanField(default=True)
    is_bestseller = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    is_new_release = models.BooleanField(default=False)
    
    # 3D Model file URL
    model_3d_url = models.CharField(max_length=500, default="/models/shoe.glb", blank=True)
    
    # Ratings
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=4.9)
    review_count = models.PositiveIntegerField(default=128)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class SneakerSize(models.Model):
    sneaker = models.ForeignKey(SneakerModel, on_delete=models.CASCADE, related_name='sizes')
    size_uk = models.CharField(max_length=10) # e.g. "UK 6", "UK 7.5", "UK 10"
    stock_quantity = models.PositiveIntegerField(default=25)

    class Meta:
        unique_together = ('sneaker', 'size_uk')
        ordering = ['size_uk']

    def __str__(self):
        return f"{self.sneaker.name} - {self.size_uk} ({self.stock_quantity} in stock)"

class ProductImage(models.Model):
    sneaker = models.ForeignKey(SneakerModel, on_delete=models.CASCADE, related_name='images')
    image_url = models.URLField(max_length=500)
    angle_label = models.CharField(max_length=50, blank=True) # e.g. "Lateral Profile", "Top View", "Heel"
    is_primary = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'id']

    def __str__(self):
        return f"{self.sneaker.name} Image ({self.angle_label})"
