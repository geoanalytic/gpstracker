from django.db import models

# Create your models here.
# This is an auto-generated Django model module created by ogrinspect.
from django.contrib.gis.db import models

class bf_road_arc(models.Model):
    feature_co = models.CharField(max_length=10)
    feature_ty = models.CharField(max_length=30)
    name = models.CharField(max_length=80)
    width = models.FloatField()
    source = models.CharField(max_length=6)
    capture_da = models.DateField()
    dispositio = models.FloatField()
    disposit_1 = models.CharField(max_length=6)
    bf_id = models.FloatField()
    shape_stle = models.FloatField()
    shape_st_1 = models.FloatField()
    shape_st_2 = models.FloatField()
    objectid = models.IntegerField()
    geom = models.MultiLineStringField(srid=4269)

# Auto-generated `LayerMapping` dictionary for BF_ROAD_ARC model
bf_road_arc_mapping = {
    'feature_co' : 'FEATURE_CO',
    'feature_ty' : 'FEATURE_TY',
    'name' : 'NAME',
    'width' : 'WIDTH',
    'source' : 'SOURCE',
    'capture_da' : 'CAPTURE_DA',
    'dispositio' : 'DISPOSITIO',
    'disposit_1' : 'DISPOSIT_1',
    'bf_id' : 'BF_ID',
    'shape_stle' : 'SHAPE_STLe',
    'shape_st_1' : 'SHAPE_ST_1',
    'shape_st_2' : 'SHAPE_ST_2',
    'objectid' : 'OBJECTID',
    'geom' : 'MULTILINESTRING',
}

class canvec_style_def(models.Model):
    shortname          = models.CharField(max_length=80)
    category           = models.CharField(max_length=80)
    description        = models.CharField(max_length=250)
    geom_outcolor      = models.CharField(max_length=80)
    geom_width         = models.FloatField()
    geom_symbol        = models.CharField(max_length=80)
    polyfill_symbol    = models.CharField(max_length=80)
    polyfill_fillcolor = models.CharField(max_length=80)
    polyfill_angle     = models.FloatField()
    polyfill_hatchgap  = models.FloatField()
    polyfill_hatchthick = models.IntegerField()
    label_font         = models.CharField(max_length=80)
    label_fillcolor    = models.CharField(max_length=80)
    label_outcolor     = models.CharField(max_length=80)
    label_height       = models.IntegerField()