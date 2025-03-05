from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, filters
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from rest_framework.pagination import PageNumberPagination
from ..models import User, Worker
from ..serializers import WorkerSerializer, UserSerializer, auth_serializer, CreateWorkerSerializer, CourseSerializer
from rest_framework.permissions import IsAdminUser

class TeacherApiView(APIView):
    
    permission_classes = [IsAdminUser]

    pagination_class = PageNumberPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ['user__phone', 'user__full_name']

    @swagger_auto_schema(request_body=CreateWorkerSerializer)
    def post(self, request):
        serializer = CreateWorkerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'status': True, 'detail':'Teacher account created'}, status=status.HTTP_201_CREATED)
        return Response({'status': False, 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        teachers = Worker.objects.all()
        serializer = WorkerSerializer(teachers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)







class WorkerCoursesAPIView(APIView):
    def get(self, request, worker_id):
        worker = get_object_or_404(Worker, id=worker_id)
        courses = worker.course.all()
        serializer = CourseSerializer(courses, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
