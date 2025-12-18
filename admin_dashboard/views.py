from django.shortcuts import render
from  rest_framework.response import Response
from rest_framework import permissions,status
from medicals.models import CustomUser
from products.models import Products
from orders.models import Order,OrderItem
from rest_framework.views import APIView

# Create your views here.

class AdminDashboardView(APIView):
    permission_classes=[permissions.IsAdminUser]

    def get(self,request):
        users_count=CustomUser.objects.filter(is_staff=False).count()
        products_count=Products.objects.count()
        orders=Order.objects.prefetch_related('items__product')

        orders_count=orders.count()
        total_income=sum(order.total_amount for order in orders)


        order_data=[]

        for order in orders:
            items=[]
            for item in order.items.all():
                items.append({
                    'name':item.product.name,
                    'price':float(item.price),
                    'quantity':item.quantity,

                })
            
            order_data.append({
                'id':order.order_id,
                'status':order.status,
                'totalAmount':float(order.total_amount),
                'items':items,
            })
            
        return Response({
            'summary':{
                "users": users_count,"products": products_count,"orders": orders_count,"income": float(total_income),
            },
            "orders": order_data
        }, status=status.HTTP_200_OK)

