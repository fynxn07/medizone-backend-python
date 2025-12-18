from django.urls import path
from .views import OrderListView,OrderSummaryView,PlaceOrderView

urlpatterns=[
    path('summary/',OrderSummaryView.as_view(),name='order-summary'),
    path('orders/',OrderListView.as_view(),name='order_list'),
    path('place_orders/',PlaceOrderView.as_view(),name='order_lists'),
]