from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status,permissions
from rest_framework.views import APIView
from orders.models import Order
from .serializers import AdminOrderSerializer
# Create your views here.


class AdminOrderListView(APIView):
    permission_classes=[permissions.IsAdminUser]

    def get(self,request):
        order=(
            Order.objects.all().select_related('user').prefetch_related('items__product').order_by('-created_at')
        )

        serializer=AdminOrderSerializer(order,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    

class AdminOrderUpdateView(APIView):
    permission_classes=[permissions.IsAdminUser]

    def patch(self,request,user_id,order_id):
        try:
            order=Order.objects.get(order_id=order_id,user__id=user_id)
        except Order.DoesNotExist:
            return Response({'detail':'Order Not Found'},status=status.HTTP_404_NOT_FOUND)
        
        new_status=request.data.get('status')

        valid_status=['Pending', 'Shipped', 'Delivered', 'Cancelled']

        if new_status not in valid_status:
            return Response({'detail':'Invalid status value'},status=status.HTTP_400_BAD_REQUEST)
        
        if order.status in ['Delivered', 'Cancelled']:
            return Response(
                {"detail": f"{order.status} orders cannot be modified"},
                status=status.HTTP_400_BAD_REQUEST
            )

        order.status=new_status
        order.save(update_fields=['status'])

        return Response({"detail":"Order status updated successfully"},status=status.HTTP_200_OK)
