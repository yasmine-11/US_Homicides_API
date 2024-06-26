from django.contrib import admin
from homicides_api.models import *

admin.site.register(Victim)
admin.site.register(Location)
admin.site.register(Disposition)
admin.site.register(Homicide)
