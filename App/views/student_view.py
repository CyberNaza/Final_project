from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action

from rest_framework import status, filters, viewsets
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from rest_framework.pagination import PageNumberPagination
from ..models import User, Student, Parents
from ..serializers import CreateStudentSerializer, ParentsSerializer, StudentSerializer
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from rest_framework.pagination import PageNumberPagination

class StudentPagination(PageNumberPagination):
    page_size = 10 
    page_size_query_param = 'page_size' 
    max_page_size = 100

# class StudentApiView(APIView):
#     permission_classes = [IsAdminUser]
#     pagination_class = PageNumberPagination
#     filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
#     search_fields = ['user__phone', 'user__full_name']

#     @swagger_auto_schema(request_body=CreateStudentSerializer)
#     def post(self, request):
#         serializer = CreateStudentSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response({'status': True, 'detail': "Student account created"}, status=status.HTTP_201_CREATED)
#         return Response({'status': False, 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

#     def get(self, request):
#         students = Student.objects.all()
#         serializer = CreateStudentSerializer(students, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)

#     @swagger_auto_schema(request_body=CreateStudentSerializer)
#     def put(self, request, student_id):
#         student = get_object_or_404(Student, id=student_id)
#         serializer = CreateStudentSerializer(student, data=request.data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response({'status': True, 'detail': "Student account updated"}, status=status.HTTP_200_OK)
#         return Response({'status': False, 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)




class StudentApiViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = CreateStudentSerializer
    permission_classes = [IsAdminUser]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ['user__phone', 'user__full_name']
    pagination_class = StudentPagination  

    @action(detail=False, methods=['get'])
    def student_list(self, request):
        """Custom endpoint to return only students where user.is_student=True"""
        users = User.objects.filter(is_student=True)  # Get users who are students
        students = Student.objects.filter(user__in=users)  # Get related Student objects

        page = self.paginate_queryset(students)
        if page is not None:
            serializer = StudentSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        else:
            serializer = StudentSerializer(students, many=True)
            return Response(serializer.data)
        
class ParentsViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser]
    
    queryset = Parents.objects.all()
    serializer_class = ParentsSerializer