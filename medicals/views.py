from django.shortcuts import render
from .models import CustomUser
from .serializers import RegisterSerializer,UserSerializer,LoginSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status,permissions
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate,get_user_model
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from  django.utils.encoding import force_str,force_bytes
from django.core.mail import send_mail
from django.conf import settings
from rest_framework.exceptions import AuthenticationFailed


# Create your views here.

User=get_user_model()
token_generator=PasswordResetTokenGenerator()

class RegisterView(APIView):
    permission_classes=[permissions.AllowAny]
    def post(self,request):
        serializer=RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user=serializer.save()
            return Response(
                {'message':'user-registered successfully',
                 'user':UserSerializer(user).data},
                 status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)



class LoginView(APIView):
    permission_classes=[permissions.AllowAny]

    def post(self,request):
        serializer=LoginSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        
        username=serializer.validated_data['username']
        password=serializer.validated_data['password']

        user=authenticate(username=username,password=password)

        if user is None:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        
        if getattr(user,'isBlock',False):
            return Response(status=status.HTTP_403_FORBIDDEN)
        
        refresh=RefreshToken.for_user(user)

        response=Response({
            'access':str(refresh.access_token),
            'user':UserSerializer(user).data
        },
        status=status.HTTP_200_OK)

        response.set_cookie(
            key='refresh_token',
            value=str(refresh),
            httponly=True,
            samesite='None',
            secure=True
        )
        return response
    
    
class SelfView(APIView):
    permission_classes=[permissions.IsAuthenticated]
    def get(self,request):
        serializer=UserSerializer(request.user)
        return Response(serializer.data,status=status.HTTP_200_OK)

    def patch(self,request):
        serializer=UserSerializer(request.user,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    

    


class LogoutView(APIView):
    permission_classes=[permissions.AllowAny]

    def post(self,request):
        try:
            refresh_token = request.COOKIES.get("refresh_token")
            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()
        except Exception:
            pass


        response=Response({"message": "Logged out successfully"},status=status.HTTP_200_OK)

        response.delete_cookie('refresh_token')

        return response


class passwordResetView(APIView):
    permission_classes=[permissions.AllowAny]


    def post(self, request):
        email = request.data.get("email")
        if not email:
            return Response({"detail": "Email is required"}, status=status.HTTP_400_BAD_REQUEST)

        
        user = User.objects.filter(email=email).first()
        if not user:
            return Response(
                {"detail": "If this email exists, a reset link has been sent."},
                status=status.HTTP_200_OK
            )
        
        uidb64=urlsafe_base64_encode(force_bytes(user.pk))
        token=token_generator.make_token(user)

        reset_link=  f"http://localhost:5174/reset-password/{uidb64}/{token}"


        send_mail(
            subject="Reset Your Password",
            message=f"Reset your password using this link: {reset_link}",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email],
            fail_silently=False,
        )

                
        return Response(
            {"detail": "If this email exists, a reset link has been sent."},
            status=status.HTTP_200_OK
        )

    
    


class passwordResetConfirmView(APIView):
    permission_classes=[permissions.AllowAny]

    def post(self,request,uidb64,token):
        token = token.strip()
        password=request.data.get('password')
        confirm_password=request.data.get('confirmPassword')

        if not password or not confirm_password:
            return Response({"detail": "Password and confirmPassword are required."},status=status.HTTP_400_BAD_REQUEST)
        if password !=confirm_password:
            return Response( {"detail": "Passwords do not match."},status=status.HTTP_400_BAD_REQUEST)

        try:
            uid=force_str(urlsafe_base64_decode(uidb64))
            user=User.objects.get(pk=uid)
        except(User.DoesNotExist,ValueError,TypeError,OverflowError):
            return Response({"detail": "Invalid reset link."},status=status.HTTP_400_BAD_REQUEST)
        
        if not token_generator.check_token(user,token):
            return Response( {"detail": "Invalid or expired token."},status=status.HTTP_400_BAD_REQUEST)
        
        user.set_password(password)
        user.save()

        return Response({"detail": "Password reset successful."},status=status.HTTP_200_OK)


   
class RefreshView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        refresh_token = request.COOKIES.get("refresh_token")

        if not refresh_token:
            raise AuthenticationFailed("No refresh token")

        try:
            refresh = RefreshToken(refresh_token)
            access_token = str(refresh.access_token)
        except Exception:
            raise AuthenticationFailed("Invalid refresh token")

        return Response({
            "access": access_token
        }, status=status.HTTP_200_OK)
  
