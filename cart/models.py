from django.db import models
from products.models import Products
from medicals.models import CustomUser

# Create your models here.
class Cart(models.Model):
    user=models.ForeignKey(CustomUser,related_name='cart_items',on_delete=models.CASCADE)
    product=models.ForeignKey(Products,related_name='cart_items',on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField(default=1)
    added_at=models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together=("user","product")

    def __str__(self):
        return f"{self.user.username} - {self.product.name} ({self.quantity})"