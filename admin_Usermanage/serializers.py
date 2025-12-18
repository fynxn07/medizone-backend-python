from rest_framework import serializers
from medicals.models import CustomUser

class AdminUserSerializer(serializers.ModelSerializer):
    class Meta:
        model=CustomUser
        fields=[
            'id','username','email','isBlock','is_staff',
        ]