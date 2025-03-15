from rest_framework import serializers
from django.contrib.auth import authenticate
from ..models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "phone", "full_name", "is_active", "is_staff", "is_admin", "is_student", "is_teacher", "created", "updated"]



class LoginSerializer(serializers.Serializer):
    phone = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        phone = data.get("phone")
        password = data.get("password")

        user = authenticate(phone=phone, password=password)
        if not user:
            raise serializers.ValidationError("Invalid phone number or password")

        return user
