from django.db import models
from cloudinary.models import CloudinaryField

# Create your models here.
class Products(models.Model):
    name=models.CharField(max_length=100)
    category=models.CharField(max_length=100)
    description=models.TextField(blank=True)
    price=models.DecimalField(max_digits=10,decimal_places=2)
    stock=models.PositiveIntegerField(default=0)
    image=CloudinaryField('product_image', blank=True, null=True)
    is_active=models.BooleanField(default=True)
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name