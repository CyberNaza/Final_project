from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views.teacher_view import TeacherApiViewSet
from .views.student_view import StudentApiViewSet, ParentsApiView
from .views import (
    GroupView, StudentsByRegistrationView, TableListCreateView,
    TableRetrieveUpdateDestroyView, DepartmentListCreateView,
    CourseListCreateView, WorkerGroupsAPIView
)

# Register ViewSets
router = DefaultRouter()
router.register(r'teachers', TeacherApiViewSet, basename='teacher')
router.register(r'students', StudentApiViewSet, basename='student')

urlpatterns = [
    path('', include(router.urls)),  # This automatically adds students/ and teachers/
    # path('status/', StudentsByRegistrationView.as_view(), name='studentbyregister'),
    path('parents/', ParentsApiView.as_view(), name="parents"),

    path('groups/', GroupView.as_view(), name='group-list'),
    path('groups/<int:group_id>/', GroupView.as_view(), name='group-detail'),

    path('tables/', TableListCreateView.as_view(), name='table-list-create'),
    path('tables/<int:pk>/', TableRetrieveUpdateDestroyView.as_view(), name='table-detail'),

    path('departments/', DepartmentListCreateView.as_view(), name='department-list-create'),

    path('courses/', CourseListCreateView.as_view(), name='course-list-create'),

    path('worker/<int:worker_id>/group/', WorkerGroupsAPIView.as_view(), name='worker-courses'),
]
