from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, filters
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from rest_framework.pagination import PageNumberPagination
from ..models import User, Worker, Group
from ..serializers import WorkerSerializer, UserSerializer, auth_serializer, CreateWorkerSerializer, CourseSerializer, GroupSerializer
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
    

    @swagger_auto_schema(request_body=CreateWorkerSerializer)
    def put(self, request, teacher_id):
        teacher = get_object_or_404(Worker, id=teacher_id)
        serializer = CreateWorkerSerializer(teacher, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'status': True, 'detail': "Teacher account updated"}, status=status.HTTP_200_OK)
        return Response({'status': False, 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class WorkerGroupsAPIView(APIView):
    def get(self, request, worker_id):
        try:
            worker = Worker.objects.get(id=worker_id)

            groups = Group.objects.filter(teacher=worker)

            serializer = GroupSerializer(groups, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Worker.DoesNotExist:
            return Response({"error": "Worker not found"}, status=status.HTTP_404_NOT_FOUND)





