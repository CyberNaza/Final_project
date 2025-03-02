from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, filters
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from rest_framework.pagination import PageNumberPagination
from ..models import User, Worker
from ..serializers import WorkerSerializer, WorkerAllSerializer, UserSerializer, auth_serializer

class AddTeacherApiView(APIView):
    pagination_class = PageNumberPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ['user__phone', 'user__full_name']

    @swagger_auto_schema(request_body=WorkerAllSerializer)
    def post(self, request):
        try:
            user_data = request.data.get('user', {})
            worker_data = request.data.get('worker', {})

            user_serializer = UserSerializer(data=user_data)
            if user_serializer.is_valid(raise_exception=True):
                user_instance = user_serializer.save()

            worker_data['user'] = user_instance.id  
            worker_serializer = WorkerSerializer(data=worker_data)

            if worker_serializer.is_valid(raise_exception=True):
                worker_serializer.save()
                return Response({'status': True, 'detail': "Account created"}, status=status.HTTP_201_CREATED)

            return Response({'status': False, 'detail': "Worker data invalid"}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({'status': False, 'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get(self, request):
        teachers = Worker.objects.all()
        serializer = WorkerSerializer(teachers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
