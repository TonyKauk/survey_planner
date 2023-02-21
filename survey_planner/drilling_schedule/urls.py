from django.urls import path

from . import views

app_name = 'drilling_schedule'

urlpatterns = [
    path('test/', views.test, name='test'),
]
