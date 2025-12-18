from django.urls import path
from .views import AdminOrderListView,AdminOrderUpdateView

urlpatterns=[
    path('admin_orders/',AdminOrderListView.as_view()),
    path('admin_order_update/<int:user_id>/<str:order_id>/',AdminOrderUpdateView.as_view())
]