from .models import Tram,Sensor
from rest_framework import serializers

class SensorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sensor
        fields = '__all__'


