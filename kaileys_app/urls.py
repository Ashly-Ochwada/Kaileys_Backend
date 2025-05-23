<<<<<<< HEAD
# from django.urls import path
# from .views import (
#     VerifyAccessCodeView,
#     CheckAccessStatusView,
#     OrganizationListView,
#     CourseListView,
#     TraineeListView,
# )

# urlpatterns = [
#     path('verify-access/', VerifyAccessCodeView.as_view(), name='verify-access'),
#     path('check-access/', CheckAccessStatusView.as_view(), name='check-access'),
#     path('organizations/', OrganizationListView.as_view(), name='organizations'),
#     path('courses/', CourseListView.as_view(), name='courses'),
#     path('trainees/', TraineeListView.as_view(), name='trainees'),
# ]

from django.urls import path
from .views import (
    APIRootView,
=======
from django.urls import path
from .views import (
>>>>>>> 79ed81e (added urls)
    VerifyAccessCodeView,
    CheckAccessStatusView,
    OrganizationListView,
    CourseListView,
    TraineeListView,
)

urlpatterns = [
<<<<<<< HEAD
    path('', APIRootView.as_view(), name='api-root'),  # this is `api/kaileys/`
=======
>>>>>>> 79ed81e (added urls)
    path('verify-access/', VerifyAccessCodeView.as_view(), name='verify-access'),
    path('check-access/', CheckAccessStatusView.as_view(), name='check-access'),
    path('organizations/', OrganizationListView.as_view(), name='organizations'),
    path('courses/', CourseListView.as_view(), name='courses'),
    path('trainees/', TraineeListView.as_view(), name='trainees'),
]
