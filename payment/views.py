from django.shortcuts import render

# Create your views here.
import razorpay
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Order


class CreateRazorpayOrder(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        amount = request.data.get("amount")

        if not amount:
            return Response(
                {"error": "Amount is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            amount = float(amount)
        except:
            return Response(
                {"error": "Invalid amount"},
                status=status.HTTP_400_BAD_REQUEST
            )

       
        client = razorpay.Client(
            auth=(
                settings.RAZORPAY_KEY_ID,
                settings.RAZORPAY_KEY_SECRET
            )
        )

        razorpay_order = client.order.create({
            "amount": int(amount * 100),  
            "currency": "INR",
            "payment_capture": 1
        })

        
        order = Order.objects.create(
            user=request.user,
            total_amount=amount,
            payment_method="ONLINE",
            payment_status="PENDING",
            razorpay_order_id=razorpay_order["id"]
        )

        return Response({
            "key": settings.RAZORPAY_KEY_ID,
            "order_id": razorpay_order["id"],
            "amount": razorpay_order["amount"],
            "order_db_id": order.id
        }, status=status.HTTP_200_OK)


class VerifyRazorpayPayment(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data

        required_fields = [
            "razorpay_order_id",
            "razorpay_payment_id",
            "razorpay_signature"
        ]

        for field in required_fields:
            if field not in data:
                return Response(
                    {"error": f"{field} is required"},
                    status=status.HTTP_400_BAD_REQUEST
                )

        client = razorpay.Client(
            auth=(
                settings.RAZORPAY_KEY_ID,
                settings.RAZORPAY_KEY_SECRET
            )
        )

        try:
         
            client.utility.verify_payment_signature({
                "razorpay_order_id": data["razorpay_order_id"],
                "razorpay_payment_id": data["razorpay_payment_id"],
                "razorpay_signature": data["razorpay_signature"],
            })

            
            order = Order.objects.get(
                razorpay_order_id=data["razorpay_order_id"]
            )

            order.payment_status = "SUCCESS"
            order.razorpay_payment_id = data["razorpay_payment_id"]
            order.save()

           

            return Response({
                "message": "Payment verified successfully",
                "order_id": order.id
            }, status=status.HTTP_200_OK)

        except razorpay.errors.SignatureVerificationError:
            return Response(
                {"error": "Payment verification failed"},
                status=status.HTTP_400_BAD_REQUEST
            )
