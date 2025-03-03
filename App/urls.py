from django.urls import path, include
from .views.teacher_view import TeacherApiView
from .views.student_view import StudentApiView
from .views import GroupView
urlpatterns = [
    path("workers/create/", TeacherApiView.as_view(), name='teacher-api'),
    path("student/create/", StudentApiView.as_view(), name='studnet-api'),


    path('groups/', GroupView.as_view()), 
    path('groups/<int:group_id>/', GroupView.as_view()),
]


