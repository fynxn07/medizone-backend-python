from django.db import models
from medicals.models import CustomUser
from products.models import Products
import uuid

# Create your models here.

class Order(models.Model):
    PAYMENT_CHOICES=[
        ('cod','Cash on Delivery'),
        ('online','Online Payment'),
    ]

    STATUS_CHOICES=[
        ("Pending","Pending"),
        ("Shipped","Shipped"),
        ("Delivered","Delivered"),
        ("Cancelled","Cancelled"),
    ]

    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='orders')
    order_id=models.CharField(max_length=50,unique=True)
    full_name=models.CharField(max_length=200)
    phone=models.CharField(max_length=20)
    address=models.TextField()
    pincode=models.CharField(max_length=20)

    payment_method=models.CharField(max_length=10,choices=PAYMENT_CHOICES,default='cod')
    total_amount=models.DecimalField(max_digits=10,decimal_places=2)
    status=models.CharField(max_length=20,choices=STATUS_CHOICES,default='Pending')
    created_at=models.DateTimeField(auto_now_add=True)

    def save(self,*args,**kwargs):
        if not self.order_id:
            self.order_id='ORD-'+ uuid.uuid4().hex[:6].upper()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.order_id


class OrderItem(models.Model):
    order=models.ForeignKey(Order,on_delete=models.CASCADE,related_name='items')
    product=models.ForeignKey(Products,on_delete=models.PROTECT)
    quantity=models.PositiveIntegerField(default=1)
    price=models.DecimalField(max_digits=10,decimal_places=2)

    def __str__(self):
        return f"{self.order.order_id} - {self.product.name} x {self.quantity}"