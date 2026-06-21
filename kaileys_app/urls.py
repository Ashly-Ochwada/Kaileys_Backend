from django.urls import path
from .views import (
    APIRootView,
    VerifyAccessView,
    RegisterTraineeView,
    OrganizationListView,
    CourseListView,
    TraineeListView,
)

urlpatterns = [
    path('', APIRootView.as_view(), name='api-root'),
    path('verify-access/', VerifyAccessView.as_view(), name='verify-access'),
    path('register-trainee/', RegisterTraineeView.as_view(), name='register-trainee'),
    path('organizations/', OrganizationListView.as_view(), name='organizations'),
    path('courses/', CourseListView.as_view(), name='courses'),
    path('trainees/', TraineeListView.as_view(), name='trainees'),
]