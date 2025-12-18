from rest_framework import serializers
from .models import Products

class ProductSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    isActive = serializers.BooleanField(source="is_active")
    class Meta:
        model=Products
        fields=[
            "id",
            "name",
            "category",
            "price",
            "stock",
            "description",
            "image",
            "isActive",      
            "created_at",
        ]

    def get_image(self, obj):
        if obj.image:
            return obj.image.url  
        return None