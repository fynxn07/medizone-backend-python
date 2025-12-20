from django.urls import path
from .views import ProductView,ProductDetails

urlpatterns=[
    path('products/',ProductView.as_view(),name='product-list'),
    path('products/<int:pk>/',ProductDetails.as_view(),name='product-detail')
]