from django.urls import path
from .views import WishlistView,WishlistAdd,WishlistRemove

urlpatterns=[
    path('wishlist/',WishlistView.as_view(),name='wishlist-view'),
    path('wishlist_add/',WishlistAdd.as_view(),name='wishlist-add'),
    path('wishlist_remove/',WishlistRemove.as_view(),name='wishlist-remove'),

]