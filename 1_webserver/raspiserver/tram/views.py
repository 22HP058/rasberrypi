from rest_framework import generics

from .models import Tram
from .serializers import TramSerializer

class TramList(generics.ListAPIView):
    queryset = Tram.objects.order_by('-date','-time')[0:50]
    serializer_class = TramSerializer

