from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.db.models import Q
from .models import Products
from .serializers import ProductSerializer


class ProductView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        search = request.GET.get("search", "")

        products = Products.objects.filter(is_active=True)

        if search:
            products = products.filter(
                Q(name__icontains=search) |
                Q(category__icontains=search) |
                Q(description__icontains=search)
            )

        products = products.order_by('created_at')
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProductDetails(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, pk):
        product = get_object_or_404(Products, pk=pk, is_active=True)
        serializer = ProductSerializer(product)
        return Response(serializer.data, status=status.HTTP_200_OK)
