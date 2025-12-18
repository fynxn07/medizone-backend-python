from django.urls import path
from .views import CartView,CartUpdateView,CartAddView,CartRemoveView

urlpatterns=[
    path('cart_list/',CartView.as_view(),name='cart-list'),
    path('cart_add/',CartAddView.as_view(),name='cart-add'),
    path('cart_update/',CartUpdateView.as_view(),name='cart-update'),
    path('cart_remove/',CartRemoveView.as_view(),name='cart-remove'),
]