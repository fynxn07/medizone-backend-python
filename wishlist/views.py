from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from .serializers import WishlistSerializer
from rest_framework import status,permissions
from .models import Wishlist
from products.models import Products
from rest_framework.views import APIView

# Create your views here.
class WishlistView(APIView):
    permission_classes=[permissions.IsAuthenticated]

    def get(self,request):
        wishlist=Wishlist.objects.filter(user=request.user).select_related('product')
        serializer=WishlistSerializer(wishlist,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
class WishlistAdd(APIView):
    permission_classes=[permissions.IsAuthenticated]
    
    def post(self,request):
        product_id=request.data.get('product_id')

        if not product_id:
            return Response({'detail':'product_id is required'},status=status.HTTP_400_BAD_REQUEST)
        
        product=get_object_or_404(Products,pk=product_id,is_active=True)

        wishlist_items,created=Wishlist.objects.get_or_create(
            user=request.user,
            product=product
        )
        serializer=WishlistSerializer(wishlist_items)
        return Response(serializer.data,status=status.HTTP_201_CREATED)


class WishlistRemove(APIView):
    permission_classes=[permissions.IsAuthenticated]

    def delete(self,request):
        product_id=request.data.get('product_id') or request.query_params.get('product_id')

        if not product_id:
            return Response({'detail':'product_id is required'},status=status.HTTP_404_NOT_FOUND)
        
        deleted, _ = Wishlist.objects.filter(user=request.user,product_id=product_id).delete()

        if deleted==0:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        return Response( {'detail': 'item removed from wishlist'},status=status.HTTP_200_OK)
