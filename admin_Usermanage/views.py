from django.shortcuts import render
from rest_framework.response import Response
from medicals.models import CustomUser
from .serializers import AdminUserSerializer
from rest_framework import permissions,status
from rest_framework.views import APIView
from django.db.models import Q

# Create your views here.

class AdminUserListView(APIView):
    permission_classes=[permissions.IsAdminUser]

    def get(self,request):
        search=request.query_params.get("search","")
        users=CustomUser.objects.filter(is_staff=False).order_by('created_at')

        if search:
            users=users.filter(
                Q(username__icontains=search) |
                Q(email__icontains=search)
            )


        serializer=AdminUserSerializer(users,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    

class AdminBlockUserView(APIView):
    permission_classes=[permissions.IsAdminUser]

    def patch(self,request,pk):
        try:
            user=CustomUser.objects.get(pk=pk,is_staff=False)
        except CustomUser.DoesNotExist:
            return Response({'detail':'User Not Found'},status=status.HTTP_404_NOT_FOUND)
        
        is_block=request.data.get('isBlock')
        if is_block is None:
            return Response({'detail':'isBlock is required'},status=status.HTTP_400_BAD_REQUEST)
        
        user.isBlock=is_block
        user.save()

        serializer=AdminUserSerializer(user)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    

