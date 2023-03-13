from django.urls import include, path
from rest_framework import routers

from . import views


app_name = 'api'

router = routers.DefaultRouter()
router.register('schedules', views.DrillingScheduleViewSet)
router.register(
    r'schedules/(?P<schedule_id>\d+)/operations',
    views.OperationViewSet, basename='operations',
)

urlpatterns = [
    path('', include(router.urls)),
]
