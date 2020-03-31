from django.contrib import admin
from .models import *

admin.site.register(Devices)
admin.site.register(Logging)
admin.site.register(Buildings)
admin.site.register(Rooms)

