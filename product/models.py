from django.db import models
from accounts.models import User, SkinType

class Brand(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class ProductType(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=200)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    product_type = models.ForeignKey(ProductType, on_delete=models.CASCADE)
    ingredients = models.TextField(null=True)
    suitable_skin_types = models.ManyToManyField(SkinType)
    ph = models.FloatField(null=True, blank=True)
    frequency_of_use = models.CharField(max_length=100)
    instruction = models.CharField(max_length=200, null=True, blank=True)
    side_effects = models.TextField(null=True, blank=True)
    price = models.BigIntegerField(help_text="Price in Vietnamese Dong (VND)")
    image = models.ImageField(default='product_images/default_product.jpg', upload_to='product_images/')
    description = models.TextField()
    pros = models.TextField(null=True, blank=True)
    cons = models.TextField(null=True, blank=True)
    recommended_age = models.CharField(max_length=50)
    is_natural_organic = models.BooleanField(default=False)
    has_fragrance = models.BooleanField(default=False)
    is_cruelty_free = models.BooleanField(default=False)
    is_oil_free = models.BooleanField(default=False)
    product_url = models.URLField()
    avg_rating = models.FloatField(default=0)

    def __str__(self):
        return self.name

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    rating = models.IntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s review of {self.product.name}"

class UserProduct(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    assigned_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product')

    def __str__(self):
        return f"{self.product.name} assigned to {self.user.username}"