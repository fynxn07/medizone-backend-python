from rest_framework import serializers
from products.models import Products

class ProductCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model=Products
        fields=[
            'name','category','price','stock','description','image','is_active',
        ]
        extra_kwargs = {
            'is_active': {'default': True}
        } 