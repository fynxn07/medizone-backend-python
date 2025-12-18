from django.shortcuts import render
from rest_framework.views import APIView
from products.models import Products
from .serializers import ProductCreateUpdateSerializer
from products.serializers import ProductSerializer 
from rest_framework.response import Response
from rest_framework import permissions,parsers,status
from .permissions import IsAdmin

# Create your views here.
class AdminProductListCreateView(APIView):
    permission_classes=[IsAdmin]
    parser_classes=[parsers.MultiPartParser,parsers.FormParser]

    def get(self,request):
        products=Products.objects.filter(is_active=True).order_by('-created_at')
        serializer=ProductSerializer(products,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    def post(self,request):
        serializer=ProductCreateUpdateSerializer(data=request.data)
        if serializer.is_valid():
            product=serializer.save(is_active=True)
              # Return with read serializer (with image URL, isActive etc.)
            read_serializer=ProductSerializer(product)
            return Response(read_serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    

class AdminProductDetailUpdateDeleteView(APIView):
    permission_classes=[IsAdmin]
    parser_classes=[parsers.MultiPartParser,parsers.FormParser]

    def get_object(self,pk):
        try:
            return Products.objects.get(pk=pk,is_active=True)
        except Products.DoesNotExist:
            return None
        
    def get(self,request,pk):
        product=self.get_object(pk)
        if not product:
            return Response({'detail':'product not found'},status=status.HTTP_404_NOT_FOUND)
        
        serializer=ProductSerializer(product)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    def patch(self,request,pk):
        product=self.get_object(pk)
        if not product:
            return Response({'detail':'prdouct not found'},status=status.HTTP_404_NOT_FOUND)

        serializer=ProductCreateUpdateSerializer(product,data=request.data,partial=True)
        if serializer.is_valid():
            product=serializer.save()
            read_serializer=ProductSerializer(product)
            return Response(read_serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request,pk):
        product=self.get_object(pk)
        if not product:
            return Response({'detail':'product not found'},status=status.HTTP_404_NOT_FOUND)
        
        product.is_active=False
        product.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

        

        