from django.db import models

from . import Course, Student, Group
from ..models import *


class Topics(models.Model):
    title = models.CharField(max_length=50)
    course = models.ForeignKey(Course, on_delete=models.RESTRICT)
    is_active = models.BooleanField(default=True)
    descriptions = models.CharField(max_length=500, blank=True, null=True)

    def __str__(self):
        return self.title


class GroupHomeWork(models.Model):
    group = models.ForeignKey(Group, on_delete=models.RESTRICT)
    topic = models.ForeignKey(Topics, on_delete=models.RESTRICT)
    is_active = models.BooleanField(default=True)
    descriptions = models.CharField(max_length=500, blank=True, null=True)


class HomeWork(models.Model):
    groupHomeWork = models.ForeignKey(GroupHomeWork, on_delete=models.RESTRICT)
    student = models.ForeignKey(Student, on_delete=models.RESTRICT)
    link = models.URLField()
    is_active = models.BooleanField(default=False)
    descriptions = models.CharField(max_length=500, blank=True, null=True)

class Baho(models.Model):
    student = models.OneToOneField(Student, on_delete=models.CASCADE)
    homework = models.OneToOneField(GroupHomeWork, on_delete=models.CASCADE)
    score = models.IntegerField()
    comment = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.student} - {self.score}"
