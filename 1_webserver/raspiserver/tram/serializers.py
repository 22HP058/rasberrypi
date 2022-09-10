from .models import Tram
from rest_framework import serializers

class TramSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tram
        fields = '__all__'


