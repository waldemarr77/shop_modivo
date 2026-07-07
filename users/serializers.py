from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import CustomUser


User = get_user_model()


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'phone', 'avatar', 'date_of_birth', 'city']
        read_only_fields = ['id', 'email']


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'phone', 'avatar', 'date_of_birth', 'city']


    def create(self, validated_data: dict) -> CustomUser:
        user = User.objects.create_user(
            username=validated_data.get('username'),
            email=validated_data.get('email'),
            password=validated_data.get('password'),
            phone=validated_data.get('phone'),
            avatar=validated_data.get('avatar'),
            date_of_birth=validated_data.get('date_of_birth'),
            city=validated_data.get('city'),
        )
        return user