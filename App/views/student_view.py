from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, filters
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from rest_framework.pagination import PageNumberPagination
from ..models import User, Student
from ..serializers import CreateStudentSerializer

class AddStudentApiView(APIView):
    pagination_class = PageNumberPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ['user__phone', 'user__full_name']

    @swagger_auto_schema(request_body=CreateStudentSerializer)
    def post(self, request):
        serializer = CreateStudentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'status': True, 'detail': "Student account created"}, status=status.HTTP_201_CREATED)
        return Response({'status': False, 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        students = Student.objects.all()
        serializer = CreateStudentSerializer(students, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
