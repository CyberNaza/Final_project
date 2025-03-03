from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from ..models import Group
from ..serializers import GroupSerializer
from drf_spectacular.utils import extend_schema
from drf_yasg.utils import swagger_auto_schema


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



