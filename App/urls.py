from django.urls import path, include
from .views.teacher_view import TeacherApiView
from .views.student_view import StudentApiView
urlpatterns = [
    path("workers/create/", TeacherApiView.as_view(), name='teacher-api'),
    path("student/create/", StudentApiView.as_view(), name='studnet-api'),
]
