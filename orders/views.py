from django.shortcuts import render
from .models import Order,OrderItem
from .serializers import OrderSerializer,OrderItemSerializer
from rest_framework.response import Response
from rest_framework import status,permissions
from rest_framework.views import APIView
from cart.models import Cart
from cart.serializers import CartSerializers
from django.db import transaction

# Create your views here.

class OrderSummaryView(APIView):
    permission_classes=[permissions.IsAuthenticated]
    def get(self,request) :
        cart_items=Cart.objects.filter(user=request.user).select_related('product')

        if not cart_items.exists():
            return Response({'detail':'cart is empty'},status=status.HTTP_400_BAD_REQUEST)
        
        serializers=CartSerializers(cart_items,many=True)

        subtotal = sum(item.product.price * item.quantity for item in cart_items)
        shipping = 40   
        discount=0

        total=subtotal+shipping-discount

        return Response(
            {   
                "items":serializers.data, 
                "subtotal": subtotal,
                "shipping": shipping,
                "discount": discount,
                "total": total,
            },
            status=status.HTTP_200_OK
        )
    



class OrderListView(APIView):
    permission_classes=[permissions.IsAuthenticated]

    def get(self,request):
        orders=Order.objects.filter(user=request.user).prefetch_related('items__product').order_by('-created_at')
        serializer=OrderSerializer(orders,many=True)
        return Response({'orders':serializer.data},status=status.HTTP_200_OK)
    
    
class PlaceOrderView(APIView):
    permission_classes=[permissions.IsAuthenticated]

    @transaction.atomic
    def post(self,request):
        user=request.user

        cart_items=Cart.objects.filter(user=user).select_related('product')

        if not cart_items.exists():
            return Response({'detail':'cart is empty'},status=status.HTTP_400_BAD_REQUEST)
        
        shipping_info=request.data.get('shippingInfo',{})
        payment_method=request.data.get('paymentMethod','cod')

        full_name=shipping_info.get('fullName')
        phone=shipping_info.get('phone')
        address = shipping_info.get("address")
        pincode = shipping_info.get("pincode")

        if not all([full_name,phone,address,pincode]):
            return Response(
                {'detail':'fullName, phone, address, pincode are required',},status=status.HTTP_400_BAD_REQUEST
            )
        
        total_amount = sum(item.product.price * item.quantity for item in cart_items)

        order=Order.objects.create(
            user=user,
            full_name=full_name,
            phone=phone,
            address=address,
            pincode=pincode,
            payment_method=payment_method,
            total_amount=total_amount,
        )
    
        order_items=[
            OrderItem(
                order=order,
                product=item.product,      
                quantity=item.quantity,
                price=item.product.price,
            )
            for item in cart_items
        ]


        OrderItem.objects.bulk_create(order_items)

        cart_items.delete()
        
        serializer=OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
