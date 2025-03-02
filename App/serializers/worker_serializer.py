from rest_framework import serializers

from ..models import worker


from .auth_serializer import UserSerializer
from ..models.worker import Worker, Course, Departments



class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id', 'title', 'descriptions']
        
        
        
        
class WorkerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Worker
        fields = ['user', 'departments', 'course', 'descriptions']
        
        
class DepartmantsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Departments
        fields = ['id', 'title', 'is_active', 'descriptions']



class Worker_requirment_serializer(serializers.ModelSerializer):
    class Meta:
        model = Worker
        fields = ['departments', 'course', 'descriptions']
        
        
        
class WorkerGetSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    
    class Meta:
        model = Worker
        fields = ['id', 'user', 'departments', 'course', 'descriptions']
        
        
        
class WorkerAllSerializer(serializers.Serializer):
    user = UserSerializer()
    worker = Worker_requirment_serializer()
    
