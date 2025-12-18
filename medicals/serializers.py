from rest_framework import serializers
from .models import CustomUser

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=CustomUser
        fields=[
            'id','username','email','isBlock','created_at','is_staff',
        ]
        read_only_fields = ['id', 'isBlock', 'created_at','is_staff']

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model=CustomUser
        fields=[
            "username",
            "email",
            "password",
            "password2",
        ]
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError('password do not match')
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('password2')
        password=validated_data.pop('password')
        user=CustomUser.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user
    

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

