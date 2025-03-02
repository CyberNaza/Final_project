from django.urls import path, include
from .views.teacher_view import AddTeacherApiView
from .views.student_view import AddStudentApiView
urlpatterns = [
    path("workers/create/", AddTeacherApiView.as_view(), name='teacher-api'),
    path("student/create/", AddStudentApiView.as_view(), name='studnet-api'),
]
