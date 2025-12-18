from django.urls import path
from .views import AdminUserListView,AdminBlockUserView

urlpatterns=[
    path('admin_user',AdminUserListView.as_view()),
    path('admin_user/<int:pk>/block',AdminBlockUserView.as_view()),
    
]