from django.db import models
from rest_framework import serializers
from products.models import Products
from medicals.models import CustomUser
# Create your models here.

class Wishlist(models.Model):
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='wishlist_items')
    product=models.ForeignKey(Products,on_delete=models.CASCADE,related_name='wishlisted_items')
    created_at=models.DateTimeField(auto_now_add=True)


    class Meta:
        unique_together=('user','product')

    def __str__(self): 
        return f"{self.user.username} -> {self.product.name}"

