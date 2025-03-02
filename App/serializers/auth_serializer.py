from rest_framework import serializers
from ..models import User, TokenModel


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "phone", "full_name", "is_active", "is_staff", "is_admin", "is_student", "is_teacher", "password")


class TokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = TokenModel
        fields = ["id", "date", "token", "created"]
