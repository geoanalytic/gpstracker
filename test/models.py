from django.db import models

# Create your models here.
# This is an auto-generated Django model module created by ogrinspect.
from django.contrib.gis.db import models

class BF_ROAD_ARC(models.Model):
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
    geom = models.MultiLineStringField(srid=-1)

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
