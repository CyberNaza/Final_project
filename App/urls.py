from django.urls import path, include
from .views.teacher_view import TeacherApiView
from .views.student_view import StudentApiView
from .views import GroupView
from .views import TableListCreateView, TableRetrieveUpdateDestroyView, DepartmentListCreateView, CourseListCreateView, WorkerCoursesAPIView
urlpatterns = [
    path("workers/create/", TeacherApiView.as_view(), name='teacher-api'),
    path("student/create/", StudentApiView.as_view(), name='studnet-api'),


    path('groups/', GroupView.as_view()), 
    path('groups/<int:group_id>/', GroupView.as_view()),


    path('tables/', TableListCreateView.as_view(), name='table-list-create'),
    path('tables/<int:pk>/', TableRetrieveUpdateDestroyView.as_view(), name='table-detail'),


    path('departments/', DepartmentListCreateView.as_view(), name='department-list-create'),



    path('courses/', CourseListCreateView.as_view(), name='course-list-create'),



    path('worker/<int:worker_id>/courses/', WorkerCoursesAPIView.as_view(), name='worker-courses'),
]


