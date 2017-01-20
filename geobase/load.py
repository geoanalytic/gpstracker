import os
from django.contrib.gis.utils import LayerMapping
from .models import bf_road_arc

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

import_shp = os.path.abspath(
    os.path.join('/data/rawdata/altalis/1_20k', 'BF_ROAD_ARC.shp'),
)

def run(verbose=True):
    lm = LayerMapping(
        bf_road_arc, import_shp, bf_road_arc_mapping,
        transform=False, encoding='iso-8859-1',
    )
    lm.save(strict=True)