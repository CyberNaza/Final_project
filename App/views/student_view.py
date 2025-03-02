from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, filters
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from rest_framework.pagination import PageNumberPagination

from ..models.auth import User
from ..models import Student  # Assuming you have a Student model
from ..serializers import CreateStudentSerializer, UserSerializer

class AddStudentApiView(APIView):
    pagination_class = PageNumberPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ['user__phone', 'user__full_name']

    @swagger_auto_schema(request_body=CreateStudentSerializer)
    def post(self, request):
        try:
            user_data = request.data.get('user', {})
            student_data = request.data.get('student', {})

            # Create and validate user
            user_serializer = UserSerializer(data=user_data)
            if user_serializer.is_valid(raise_exception=True):
                user_instance = user_serializer.save()

            # Set user role as student
            user_instance.is_student = True  # Assuming `is_student` exists
            user_instance.save()

            # Assign student data to the user
            student_data['user'] = user_instance.id
            student_serializer = CreateStudentSerializer(data=student_data)

            if student_serializer.is_valid(raise_exception=True):
                student_serializer.save()
                return Response({'status': True, 'detail': "Student account created"}, status=status.HTTP_201_CREATED)

            return Response({'status': False, 'detail': "Student data invalid"}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({'status': False, 'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get(self, request):
        students = Student.objects.all()
        serializer = CreateStudentSerializer(students, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)