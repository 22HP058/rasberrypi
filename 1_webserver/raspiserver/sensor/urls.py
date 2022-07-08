from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import *

urlpatterns = [
    path('sensor/',SensorList.as_view()),
    #pk가 int아님
    #path('sensor/<int:pk>/',SensorDetail.as_view())
]