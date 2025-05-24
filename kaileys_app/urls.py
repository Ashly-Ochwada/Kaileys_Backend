from django.urls import path
from .views import (
    APIRootView,
    VerifyAccessCodeView,
    CheckAccessStatusView,
    GenerateAccessCodeView,
    OrganizationListView,
    CourseListView,
    TraineeListView,
)

urlpatterns = [
    path('', APIRootView.as_view(), name='api-root'),
    path('verify-access/', VerifyAccessCodeView.as_view(), name='verify-access'),
    path('check-access/', CheckAccessStatusView.as_view(), name='check-access'),
    path('generate-access-code/', GenerateAccessCodeView.as_view(), name='generate-access-code'),
    path('organizations/', OrganizationListView.as_view(), name='organizations'),
    path('courses/', CourseListView.as_view(), name='courses'),
    path('trainees/', TraineeListView.as_view(), name='trainees'),
]