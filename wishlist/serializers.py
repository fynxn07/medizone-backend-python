from rest_framework import serializers
from .models import Wishlist
from products.serializers import ProductSerializer
from products.models import Products


class WishlistSerializer(serializers.ModelSerializer):
    product=ProductSerializer(read_only=True)


    class Meta:
        model=Wishlist
        fields=['product']
