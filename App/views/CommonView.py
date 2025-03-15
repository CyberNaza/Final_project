from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListAPIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from ..models import Group, Departments, Student, Course, AttendanceLevel, Attendance, Topics, GroupHomeWork, HomeWork, Month, Payment
# from ..serializers import GroupSerializer, DepartmentSerializer, CourseSerializer, CreateStudentSerializer, DateRangeSerializer, AttendanceSerializer, AttendanceLevelSerializer
from ..serializers import *
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, viewsets
from rest_framework import serializers
from rest_framework.decorators import api_view
from datetime import datetime
from collections import defaultdict
from rest_framework.permissions import IsAdminUser, IsAuthenticated


from ..models import Table
from ..serializers import TabelSerializer


class GroupView(APIView):
    permission_classes = [IsAdminUser]
    
    def get(self, request, group_id=None):
        """Retrieve a single group by ID or list all groups."""
        if group_id:
            group = get_object_or_404(Group, id=group_id)
            serializer = GroupSerializer(group)
        else:
            groups = Group.objects.all()
            serializer = GroupSerializer(groups, many=True)
        return Response(serializer.data)
    @swagger_auto_schema(request_body=GroupSerializer)
    def post(self, request):
        serializer = GroupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, group_id):
        group = get_object_or_404(Group, id=group_id)
        serializer = GroupSerializer(group, data=request.data, partial=True)  # Partial allows updating some fields
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, group_id):
        group = get_object_or_404(Group, id=group_id)
        group.delete()
        return Response({"message": "Group deleted successfully"}, status=status.HTTP_204_NO_CONTENT)






class TableListCreateView(APIView):
    permission_classes = [IsAdminUser]
    
    def get(self, request):
        tables = Table.objects.all()
        serializer = TabelSerializer(tables, many=True)
        return Response(serializer.data)
    @swagger_auto_schema(request_body=TabelSerializer)
    def post(self, request):
        serializer = TabelSerializer(data=request.data)
        if serializer.is_valid():
            table = serializer.save()
            return Response(TabelSerializer(table).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TableRetrieveUpdateDestroyView(APIView):
    permission_classes = [IsAdminUser]
    
    def get_object(self, pk):
        try:
            return Table.objects.get(pk=pk)
        except Table.DoesNotExist:
            return None

    def get(self, request, pk):
        table = self.get_object(pk)
        if table is None:
            return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = TabelSerializer(table)
        return Response(serializer.data)

    def put(self, request, pk):
        table = self.get_object(pk)
        if table is None:
            return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = TabelSerializer(table, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        table = self.get_object(pk)
        if table is None:
            return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)
        table.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

class AttendanceLevelViewSet(viewsets.ModelViewSet):
    
    queryset = AttendanceLevel.objects.all()
    serializer_class = AttendanceLevelSerializer

class AttendanceViewSet(viewsets.ModelViewSet):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer



class DepartmentViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser]
    
    queryset = Departments.objects.all()
    serializer_class = DepartmentSerializer

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


class StudentsByRegistrationView(APIView):
    @swagger_auto_schema(request_body=DateRangeSerializer)
    def post(self, request):
        serializer = DateRangeSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        start_date = datetime.combine(serializer.validated_data['start_date'], datetime.min.time())
        end_date = datetime.combine(serializer.validated_data['end_date'], datetime.max.time())
        
        students = Student.objects.filter(created__range=[start_date, end_date]).prefetch_related('course')
        is_studying = Student.objects.filter(is_line=True).count()
        is_compleated = Student.objects.filter(is_finished=True).count()

        
        course_summary = defaultdict(int)
        for student in students:
            for course in student.course.all():
                course_summary[course.title] += 1


        response_data = {
            'registered_by_course': [{ 'course': course, 'student_count': count } for course, count in course_summary.items()],
            'studying': is_studying,
            'compleated': is_compleated,
        }


        return Response(response_data, status=status.HTTP_200_OK)





class TopicsViewSet(viewsets.ModelViewSet):
    queryset = Topics.objects.all()
    serializer_class = TopicsSerializer


class GroupHomeWorkViewSet(viewsets.ModelViewSet):
    queryset = GroupHomeWork.objects.all()
    serializer_class = GroupHomeWorkSerializer


class HomeWorkViewSet(viewsets.ModelViewSet):
    queryset = HomeWork.objects.all()
    serializer_class = HomeWorkSerializer



class BahoViewSet(viewsets.ModelViewSet):
    queryset = Baho.objects.all()
    serializer_class = BahoSerializer






class MonthViewSet(viewsets.ModelViewSet):
    queryset = Month.objects.all()
    serializer_class = MonthSerializer


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
