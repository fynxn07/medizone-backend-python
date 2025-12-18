from .views import RegisterView,LoginView,SelfView,LogoutView,passwordResetView,passwordResetConfirmView,RefreshView
from django.urls import path

urlpatterns=[
    path('auth/register/',RegisterView.as_view(),name='auth-register'),
    path('auth/login/',LoginView.as_view(),name='auth-login'),
    path('auth/self/',SelfView.as_view(),name='auth-self'),
    path('auth/logout/',LogoutView.as_view(),name='auth-logout'),
    path('auth/password_reset/',passwordResetView.as_view(),name='password-reset'),
    path('auth/password_reset_confirm/<uidb64>/<token>',passwordResetConfirmView.as_view(),name='password-reset-confirm'),
    path("auth/refresh/", RefreshView.as_view()),


]

