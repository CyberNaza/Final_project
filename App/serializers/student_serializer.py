from django.forms import ValidationError
from rest_framework import serializers
from ..models import Student, Parents, User
from rest_framework import serializers
from ..models import User, Student

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["phone", "full_name", "password", "is_student"]
        extra_kwargs = {"password": {"write_only": True}}
        ref_name = 'StudentUserSerializer'

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        user.is_student = True  # Set user as student
        user.save()
        return user

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['phone', 'password', 'full_name']

    def create(self, validated_data):
        phone = validated_data.get("phone")
        password = validated_data.get("password")
        full_name = validated_data.get("full_name")

        # Check if user with this phone number already exists
        if User.objects.filter(phone=phone).exists():
            raise ValidationError({"phone": "This phone number is already in use."})

        # Create new user
        user = User.objects.create_user(phone=phone, password=password, full_name=full_name, is_student=True)
        return user

class ParentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parents
        fields = ['full_name', 'phone_number', 'address', 'descriptions']

class CreateStudentSerializer(serializers.ModelSerializer):
    phone = serializers.CharField(write_only=True, required=True)  # Ask for phone
    password = serializers.CharField(write_only=True, required=True)  # Ask for password
    full_name = serializers.CharField(write_only=True, required=False, allow_blank=True)  # Optional full name
    group = serializers.ListField(child=serializers.IntegerField(), write_only=True)  # Handle many-to-many
    course = serializers.ListField(child=serializers.IntegerField(), write_only=True)  # Handle many-to-many

    class Meta:
        model = Student
        fields = ['phone', 'password', 'full_name', 'is_line', 'descriptions', 'group', 'course']

    def create(self, validated_data):
        phone = validated_data.pop('phone')
        password = validated_data.pop('password')
        full_name = validated_data.pop('full_name', '')

        groups = validated_data.pop('group', [])
        courses = validated_data.pop('course', [])

        # Create user
        user = User.objects.create_user(phone=phone, password=password, full_name=full_name, is_student=True)

        # Create student linked to the user
        student = Student.objects.create(user=user, **validated_data)

        # Assign groups and courses properly
        student.group.set(groups)
        student.course.set(courses)

        return student
