from django.forms import ValidationError
from rest_framework import serializers

# from App.models.worker import Departments
from ..models import Student, Parents, User, Departments, Course
from rest_framework import serializers
from ..models import User, Worker



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["phone", "full_name", "password", "is_student"]
        extra_kwargs = {"password": {"write_only": True}}
        ref_name = 'StudentUserSerializer'

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        user.is_student = True  
        user.save()
        return user
    
class WorkerSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['phone', 'password', 'full_name']



class CreateWorkerSerializer(serializers.ModelSerializer):
    phone = serializers.CharField(write_only=True, required=True)
    password = serializers.CharField(write_only=True, required=True)
    full_name = serializers.CharField(write_only=True, required=False, allow_blank=True)
    
    departments = serializers.ListField(child=serializers.CharField(), write_only=True)  # Accepts title
    course = serializers.ListField(child=serializers.CharField(), write_only=True)  # Accepts title

    class Meta:
        model = User
        fields = ['phone', 'password', 'full_name', 'departments', 'course']

    def create(self, validated_data):
        phone = validated_data.pop('phone')
        password = validated_data.pop('password')
        full_name = validated_data.pop('full_name')

        department_titles = validated_data.pop('departments', [])
        course_titles = validated_data.pop('course', [])

        departments = []
        for title in department_titles:
            department, created = Departments.objects.get_or_create(title=title)
            departments.append(department)

        courses = []
        for title in course_titles:
            course, created = Course.objects.get_or_create(title=title)
            courses.append(course)

        user = User.objects.create_user(phone=phone, password=password, full_name=full_name, is_teacher=True)
        teacher = Worker.objects.create(user=user)

        teacher.departments.set(departments)
        teacher.course.set(courses)

        return teacher

