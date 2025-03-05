from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from ..models import Group, Departments
from ..serializers import GroupSerializer, DepartmentSerializer, CourseSerializer
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics




class GroupView(APIView):
    
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






from ..models import Table
from ..serializers import TabelSerializer

class TableListCreateView(APIView):
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
    



class DepartmentListCreateView(generics.ListCreateAPIView):
    queryset = Departments.objects.all()
    serializer_class = DepartmentSerializer



class CourseListCreateView(generics.ListCreateAPIView):
    queryset = Departments.objects.all()
    serializer_class = CourseSerializer



