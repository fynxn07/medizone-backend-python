
from rest_framework import serializers
from orders.models import Order,OrderItem

class AdminOrderItemSerializer(serializers.ModelSerializer):
    name=serializers.CharField(source='product.name')
    price=serializers.DecimalField(max_digits=10,decimal_places=2)
    image=serializers.ImageField(source='product.image')

    class Meta:
        model=OrderItem
        fields=[
            'name','price','image','quantity'
        ]


class AdminOrderSerializer(serializers.ModelSerializer):
    id=serializers.CharField(source='order_id')
    userId=serializers.IntegerField(source='user.id')
    orderDate=serializers.DateTimeField(source='created_at',format='%d/%m/%Y')

    items=AdminOrderItemSerializer(many=True,read_only=True)
    totalAmount=serializers.DecimalField(source='total_amount',max_digits=10,decimal_places=2)
    shippingInfo=serializers.SerializerMethodField()

    class Meta:
        model=Order
        fields=[
            'id','userId','orderDate','items','shippingInfo','totalAmount','status',
        ]

    def get_shippingInfo(self, obj):
        return {
            "fullName": obj.full_name,
            "address": obj.address,
            "pincode": obj.pincode,
        }
