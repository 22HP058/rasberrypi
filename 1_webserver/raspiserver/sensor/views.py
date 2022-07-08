from rest_framework import generics

from .models import Sensor
from .serializers import SensorSerializer

class SensorList(generics.ListCreateAPIView):
    queryset = Sensor.objects.all()
    serializer_class = SensorSerializer

class SensorDetail(generics.RetrieveAPIView):
    queryset = Sensor.objects.all()
    serializer_class = SensorSerializer
