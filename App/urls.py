from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView

from rest_framework.routers import DefaultRouter
from .views.teacher_view import TeacherApiViewSet
from .views.student_view import StudentApiViewSet, ParentsViewSet
from .views import (
    GroupView, StudentsByRegistrationView, TableListCreateView,
    TableRetrieveUpdateDestroyView, DepartmentViewSet,
    CourseViewSet, WorkerGroupsAPIView, AttendanceLevelViewSet,
    AttendanceViewSet, TopicsViewSet, GroupHomeWorkViewSet, HomeWorkViewSet, BahoViewSet, PaymentViewSet, MonthViewSet, 
)
from .views.auth_view import *

# Register ViewSets
router = DefaultRouter()
router.register(r'teachers', TeacherApiViewSet, basename='teacher')
router.register(r'students', StudentApiViewSet, basename='student')
router.register(r'parents', ParentsViewSet)
router.register(r'departments', DepartmentViewSet)
router.register(r'courses', CourseViewSet)
router.register(r'attendance-levels', AttendanceLevelViewSet)
router.register(r'attendance', AttendanceViewSet)
router.register(r'TopicsViewSet', TopicsViewSet)
router.register(r'GroupHomeWork', GroupHomeWorkViewSet)
router.register(r'HomeWork', HomeWorkViewSet)
router.register(r'Baholash', BahoViewSet)
router.register(r'payments', PaymentViewSet)
router.register(r'months', MonthViewSet)


urlpatterns = [
    # path('auth/login/', LoginView.as_view(), name='auth_login'),
    path('auth/me/', MeView.as_view(), name='auth_me'),
    # path('auth/token/refresh/', TokenRefreshView.as_view(), name='auth_token_refresh'),
    path('', include(router.urls)),

    # path('status/', StudentsByRegistrationView.as_view(), name='studentbyregister'),

    path('groups/', GroupView.as_view(), name='group-list'),
    path('groups/<int:group_id>/', GroupView.as_view(), name='group-detail'),

    path('tables/', TableListCreateView.as_view(), name='table-list-create'),
    path('tables/<int:pk>/', TableRetrieveUpdateDestroyView.as_view(), name='table-detail'),


    path('worker/<int:worker_id>/group/', WorkerGroupsAPIView.as_view(), name='worker-courses'),
]
