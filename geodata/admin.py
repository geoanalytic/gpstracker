from django.contrib.gis import admin

# Register your models here.

from .models import Location, Gpslocation, Device

# subclass the GeoModelAdmin to use the locally hosted OpenLayers library
class olGeoModelAdmin(admin.GeoModelAdmin):
    openlayers_url = 'OpenLayers.js'

# subclass the OSMGeoAdmin to use the locally hosted OpenLayers library
class olOSMGeoAdmin(admin.OSMGeoAdmin):
    openlayers_url = 'OpenLayers.js'

# register an admin tool for the Location model
# admin.site.register(Location, olGeoModelAdmin)

# the OSMGeoAdmin tool uses the openstreetmap data for a nicer experience
admin.site.register(Location, olOSMGeoAdmin)
admin.site.register(Gpslocation, olOSMGeoAdmin)
admin.site.register(Device)
