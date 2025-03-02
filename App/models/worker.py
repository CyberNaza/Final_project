from django.db import models
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

from .auth import User


# Markazda oqitiladigan fanlar
class Course(models.Model):
    title = models.CharField(max_length=50)
    descriptions = models.CharField(max_length=500, null=True, blank=True)

    def __str__(self):
        return self.title


# Xodimlarning darajasini belgilash uchun
class Departments(models.Model):
    title = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    descriptions = models.CharField(max_length=500, null=True, blank=True)
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ['user__phone', 'user__full_name']

    def __str__(self):
        return self.title


# Xodimlarning datalarini saqlash uchun yuqoridagi Course va Departments modellari Worker bog'langan
class Worker(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    departments = models.ManyToManyField(Departments, related_name='worker')
    course = models.ManyToManyField(Course, related_name='worker')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    descriptions = models.CharField(max_length=500, blank=True, null=True)

    def __str__(self):
        return self.user.phone
