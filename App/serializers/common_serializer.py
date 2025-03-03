from django.forms import ValidationError
from rest_framework import serializers
from ..models import Student, Parents, User, Group, Worker, Table, Course, TableType, Rooms
from django.shortcuts import get_object_or_404
from ..models.group import Table
from rest_framework import serializers



class TabelSerializer(serializers.ModelSerializer):
    room = serializers.CharField()
    type = serializers.CharField()
    start_time = serializers.TimeField()
    end_time = serializers.TimeField()

    class Meta:
        model = Table
        fields = ['room', 'type', 'start_time', 'end_time', 'descriptions']

    def create(self, validated_data):
        room_id = validated_data.get('room')
        type_id = validated_data.get('type')
        start_time = validated_data.get('start_time')
        end_time = validated_data.get('end_time')
        descriptions = validated_data.get('descriptions')

        type_instance = TableType.objects.get(id=type_id)
        room_instance = Rooms.objects.get(id=room_id)

        return Table.objects.create(
            room=room_instance,
            type=type_instance,
            start_time=start_time,
            end_time=end_time,
            descriptions=descriptions
        )

    
    










class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['title', 'price', 'descriptions', 'course', 'teacher', 'table']


    def create(self, validated_data):
        course = validated_data.get('course')
        teachers = validated_data.get('teacher', [])  # Expecting a list
        table = validated_data.get('table')

        # Ensure that teachers is a list and extract IDs
        teacher_ids = [teacher.id for teacher in teachers] if teachers else []

        # Fetch related objects safely
        course_id = course.id if course else None
        teacher_id = teacher_ids[0] if teacher_ids else None
        table_id = table.id if table else None

        course = Course.objects.get(id=course_id) if course_id else None
        table = Table.objects.get(id=table_id) if table_id else None
        teacher = Worker.objects.filter(id__in=teacher_ids) if teacher_ids else None

        group = Group.objects.create(
            title=validated_data.get('title'),
            course=course,
            price=validated_data.get('price'),
            descriptions=validated_data.get('descriptions'),
            table=table,
            )

        if teacher:
            group.teacher.set(teacher)

        return group
