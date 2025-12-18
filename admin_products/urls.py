from django.urls import path
from .views import AdminProductListCreateView,AdminProductDetailUpdateDeleteView

urlpatterns=[
    path('admin_products/',AdminProductListCreateView.as_view(),name='admin-products'),
    path('admin_products/<int:pk>/',AdminProductDetailUpdateDeleteView.as_view(),name='admin-products-details'),
]