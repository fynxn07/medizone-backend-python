from django.urls import path
from .views import CreateRazorpayOrder, VerifyRazorpayPayment

urlpatterns = [

    path("create/", CreateRazorpayOrder.as_view()),
    path("verify/", VerifyRazorpayPayment.as_view()),

]
