from django.forms import ValidationError
from rest_framework import serializers
from ..models import Student, Parents, User, Group, Worker, Table, Course
from django.shortcuts import get_object_or_404
from ..models.group import Table
from rest_framework import serializers


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
