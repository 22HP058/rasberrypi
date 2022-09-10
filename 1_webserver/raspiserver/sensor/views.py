from rest_framework import generics

from .models import Sensor
from .serializers import SensorSerializer

class SensorList(generics.ListAPIView):
    queryset = Sensor.objects.order_by('-date','-time')[0:50]
    serializer_class = SensorSerializer

