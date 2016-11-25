from django.contrib.gis import admin

# Register your models here.

from .models import Location

class olGeoModelAdmin(admin.GeoModelAdmin):
    openlayers_url = 'OpenLayers.js'

admin.site.register(Location, olGeoModelAdmin)
