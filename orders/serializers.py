from rest_framework import serializers
from .models import Order,OrderItem
from products.serializers import ProductSerializer 


class OrderItemSerializer(serializers.ModelSerializer):
    product=ProductSerializer(read_only=True)

    class Meta:
        model=OrderItem
        fields=['product','quantity','price']


class OrderSerializer(serializers.ModelSerializer):
    id = serializers.CharField(source='order_id')
    shippingInfo = serializers.SerializerMethodField()
    paymentMethod = serializers.CharField(source='payment_method')
    items = OrderItemSerializer(many=True,read_only=True)
    totalAmount = serializers.DecimalField(source='total_amount', max_digits=10, decimal_places=2)
    orderDate = serializers.DateTimeField(source='created_at', format='%m/%d/%Y')

    class Meta:
        model=Order
        fields=[ 
            'id',
            'shippingInfo',
            'paymentMethod',
            'items',
            'totalAmount',
            'orderDate',
            'status',
        ]
    
    def get_shippingInfo(self,obj):
        return{
            'fullName':obj.full_name,
            'phone':obj.phone,
            'address':obj.address,
            'pincode':obj.pincode
        }
    

    