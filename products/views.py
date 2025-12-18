from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status,permissions
from django.shortcuts import get_object_or_404
from .models import Products
from .serializers import ProductSerializer

# Create your views here.

class ProductView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self,request):
        product=Products.objects.filter(is_active=True).order_by('created_at')
        serializer=ProductSerializer(product,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    

class ProductDetails(APIView):
    permission_classes=[permissions.AllowAny]

    def get(self,request,pk):
        product=get_object_or_404(Products, pk=pk, is_active=True)
        serialzer=ProductSerializer(product)
        return Response(serialzer.data,status=status.HTTP_200_OK)
    



