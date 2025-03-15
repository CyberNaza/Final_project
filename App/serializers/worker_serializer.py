from django.forms import ValidationError
from rest_framework import serializers

# from App.models.worker import Departments
from ..models import Student, Parents, User, Departments, Course
from rest_framework import serializers
from ..models import User, Worker



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["phone", "full_name", "password", "is_teacher"]
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
            department, created = Departments.objects.get_or_create(id=title)
            departments.append(department)

        courses = []
        for title in course_titles:
            course, created = Course.objects.get_or_create(id=title)
            courses.append(course)

        user = User.objects.create_user(phone=phone, password=password, full_name=full_name, is_teacher=True)
        teacher = Worker.objects.create(user=user)

        teacher.departments.set(departments)
        teacher.course.set(courses)

        return teacher


    def update(self, instance, validated_data):
        """ Update an existing Worker and User details """
        user = instance.user  # Get the associated User object
        
        phone = validated_data.get('phone', user.phone)
        password = validated_data.get('password', None)
        full_name = validated_data.get('full_name', user.full_name)

        # Update User fields
        user.phone = phone
        if password:
            user.set_password(password)  
        user.full_name = full_name
        user.save()

        # Update Departments
        if 'departments' in validated_data:
            department_titles = validated_data['departments']
            departments = [Departments.objects.get_or_create(id=title)[0] for title in department_titles]
            instance.departments.set(departments)

        # Update Courses
        if 'course' in validated_data:
            course_titles = validated_data['course']
            courses = [Course.objects.get_or_create(id=title)[0] for title in course_titles]
            instance.course.set(courses)

        instance.save()
        return instance

class WorkerSerializer(serializers.ModelSerializer):
    phone = serializers.CharField(source='user.phone', read_only=True)
    full_name = serializers.CharField(source='user.full_name', read_only=True)
    is_teacher = serializers.BooleanField(source='user.is_teacher', read_only=True)

    class Meta:
        model = Worker
        fields = ['id', 'phone', 'full_name', 'is_teacher', 'departments', 'course']


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Departments
        fields = ['id', 'title', 'is_active', 'descriptions']
    
    def create(self, validated_data):
        return Departments.objects.create(**validated_data)
