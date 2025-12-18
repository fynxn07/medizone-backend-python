from django.shortcuts import render,get_object_or_404
from rest_framework.views import APIView
from .serializers import CartSerializers
from .models import Cart
from rest_framework import status,permissions
from products.models import Products
from rest_framework.response import Response


# Create your views here.
class CartView(APIView):
    permission_classes=[permissions.IsAuthenticated]

    def get(self,request):
        items=Cart.objects.filter(user=request.user).select_related('product')
        serializer=CartSerializers(items,many=True)
        total=sum(item.product.price * item.quantity for item in items)
        return Response({'items':serializer.data,'total':total},status=status.HTTP_200_OK)
    
class CartAddView(APIView):
    permission_classes=[permissions.IsAuthenticated]

    def post(self,request):
        product_id=request.data.get('product_id')
        quantity=request.data.get('quantity',1)

        if not product_id:
            return Response({"detail": "product_id is required"},status=status.HTTP_400_BAD_REQUEST)
        
        try:
            quantity=int(quantity)
        except ValueError:
            return Response({"detail": "quantity must be integer"},status=status.HTTP_400_BAD_REQUEST)
        
        if quantity <=0:
            return Response({"detail": "quantity must be greater than 0"},status=status.HTTP_400_BAD_REQUEST)
        
        
        product=get_object_or_404(Products,pk=product_id,is_active=True)

        cart_item,created=Cart.objects.get_or_create(user=request.user,product=product,defaults={"quantity":quantity})
        
        if not created:
            cart_item.quantity+=quantity
            cart_item.save()
        
        serializer=CartSerializers(cart_item)
        return Response(serializer.data,status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)
    

class CartUpdateView(APIView):
    permission_classes=[permissions.IsAuthenticated]

    def patch(self,request):
        product_id=request.data.get('product_id')
        quantity=request.data.get('quantity')
    
        if not product_id or quantity is None:
            return Response({"detail": "product_id and quantity are required"},status=status.HTTP_400_BAD_REQUEST)
        
        try:
            quantity=int(quantity)
        except (ValueError,TypeError):
            return Response({'detail':'quantity must be integer'},status=status.HTTP_400_BAD_REQUEST)
        
        if quantity <=0:
            deleted,_=Cart.objects.filter(user=request.user,product_id=product_id).delete()
        
            if deleted==0:
                return Response({'detail':'item not found in cart'},status=status.HTTP_404_NOT_FOUND)
        
            return Response(status=status.HTTP_200_OK)
        
        cart_item=get_object_or_404(Cart,user=request.user,product_id=product_id)
        cart_item.quantity=quantity
        cart_item.save()

        serializer=CartSerializers(cart_item)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
class CartRemoveView(APIView):
    permission_classes=[permissions.IsAuthenticated]

    def delete(self,request):
        product_id=request.data.get('product_id') or request.query_params.get('product_id')

        if not product_id:
            return Response({'detail':'product_id is required'},status=status.HTTP_400_BAD_REQUEST)
        
        deleted,_=Cart.objects.filter(user=request.user,product_id=product_id).delete()

        if deleted==0:
            return Response({'detail':'item not found'},status=status.HTTP_404_NOT_FOUND)
        
        return Response({'detail':'item removed from cart'},status=status.HTTP_200_OK)
