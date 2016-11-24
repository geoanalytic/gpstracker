from django.contrib.gis import admin

# Register your models here.

from .models import Location

admin.site.register(Location, admin.GeoModelAdmin)
