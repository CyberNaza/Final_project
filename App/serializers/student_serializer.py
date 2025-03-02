from rest_framework import serializers
from ..models import Student, Parents, User
from .auth_serializer import UserSerializer

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ["user", "group", "course"]

    def validate_user(self, value):
        if isinstance(value, dict):
            raise serializers.ValidationError("User should be an ID, not a dictionary.")
        return value



class ParentsSerializer(serializers.ModelSerializer):  # ✅ Ensure correct naming
    class Meta:
        model = Parents  # ✅ Ensure model is correctly specified
        fields = ['full_name', 'phone_number', 'address', 'descriptions']

class CreateStudentSerializer(serializers.Serializer):  # ✅ Naming convention
    user = UserSerializer()
    student = StudentSerializer()
