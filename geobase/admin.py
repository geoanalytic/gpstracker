from django.contrib.gis import admin

# Register your models here.

from .models import bf_road_arc
from .models import canvec_style_def
from .models import j_style_altalis20k

# subclass the GeoModelAdmin to use the locally hosted OpenLayers library
class olGeoModelAdmin(admin.GeoModelAdmin):
    openlayers_url = 'OpenLayers.js'

# subclass the OSMGeoAdmin to use the locally hosted OpenLayers library
class olOSMGeoAdmin(admin.OSMGeoAdmin):
    openlayers_url = 'OpenLayers.js'

# register an admin tool for the Location model
# admin.site.register(Location, olGeoModelAdmin)

# the OSMGeoAdmin tool uses the openstreetmap data for a nicer experience
admin.site.register(bf_road_arc, olOSMGeoAdmin)

admin.site.register(canvec_style_def)
admin.site.register(j_style_altalis20k)