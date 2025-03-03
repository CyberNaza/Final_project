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
        user.is_student = True  
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

        if User.objects.filter(phone=phone).exists():
            raise ValidationError({"phone": "This phone number is already in use."})


        user = User.objects.create_user(phone=phone, password=password, full_name=full_name, is_student=True)
        return user



class ParentsSerializer(serializers.ModelSerializer):

    full_name = serializers.CharField(write_only=True, required=False, allow_blank=True)
    phone = serializers.CharField(write_only=True, required=True)
    address = serializers.CharField(write_only=True, required=True)
    descriptions = serializers.CharField(write_only=True, required=True)        
    Student = serializers.CharField(write_only=True, required=True)
    class Meta:
        model = Parents
        fields = ['full_name', 'phone_number', 'address', 'descriptions', 'student']

    def create(self, validated_data):
        full_name = validated_data.pop('full_name')
        phone = validated_data.pop('phone_number')
        address = validated_data.pop('address')
        descriptions = validated_data.pop('descriptions')
        

        parents = Parents.objects.create_user(full_name=full_name, phone=phone, address=address, descriptions=descriptions)
        student = Student.objects.get()
        return parents

        


class CreateStudentSerializer(serializers.ModelSerializer):
    phone = serializers.CharField(write_only=True, required=True)
    password = serializers.CharField(write_only=True, required=True)  
    full_name = serializers.CharField(write_only=True, required=False, allow_blank=True) 
    group = serializers.ListField(child=serializers.IntegerField(), write_only=True)  
    course = serializers.ListField(child=serializers.IntegerField(), write_only=True) 

    class Meta:
        model = Student
        fields = ['phone', 'password', 'full_name', 'is_line', 'descriptions', 'group', 'course']

    def create(self, validated_data):
        phone = validated_data.pop('phone')
        password = validated_data.pop('password')
        full_name = validated_data.pop('full_name', '')

        groups = validated_data.pop('group', [])
        courses = validated_data.pop('course', [])
        departments = []

        # for title in department_titles:
        #     department, created = Departments.objects.get_or_create(title=title)
        #     departments.append(department)

        # courses = []
        # for title in course_titles:
        #     course, created = Course.objects.get_or_create(title=title)
        #     courses.append(course)

        
        user = User.objects.create_user(phone=phone, password=password, full_name=full_name, is_student=True)

        student = Student.objects.create(user=user, **validated_data)

        # Assign groups and courses properly
        student.group.set(groups)
        student.course.set(courses)

        return student
