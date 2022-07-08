from django.contrib import admin
from .models import Tram
from .models import Sensor

admin.site.register(Tram)
admin.site.register(Sensor)