'''
File: geodata/views.py
Author: David Currie
Description: Views for the gpslocations app.  Uses a GET request to record locations 
             from remote devices.
'''
from django.shortcuts import render
from django.http import HttpResponse
from django.core.serializers import serialize
import logging
from urllib.parse import unquote
from datetime import datetime
from django.contrib.gis.geos import Point, LineString

from .models import Location, Gpslocation
from .forms import Gpslocationform

# Geojson serializer for Locations
def geojsonFeedLocation(request):
    return HttpResponse(serialize('geojson', Location.objects.all(),fields=('name','mpoint')))

# A track request should include a valid coordinate plus some optional data
# use a logger for debugging the messages
logger = logging.getLogger(__name__)

def track(request):
    logger.info('Got tracking request')
    if request.method == 'GET':
        track_data = Gpslocationform(request.GET)
        if track_data.is_valid():
            track_point = track_data.save(commit=False)
            track_point.mpoint = Point(track_data.cleaned_data['longitude'], track_data.cleaned_data['latitude'])
            track_point.gpstime = datetime.strptime(unquote(track_data.cleaned_data['date']),'%Y-%m-%d+%H:%M:%S')
            track_point.save()
        else:
            logger.error('Failed to validate track data')
    else:
        logger.error('Not a GET request')

    # this function never returns anything (maybe there should be a debug statement)
    return HttpResponse('')

# Geojson serializer
def geojsonFeed(request):
    return HttpResponse(serialize('geojson', 
                        Gpslocation.objects.order_by('phonenumber','-gpstime').distinct('phonenumber'), 
                        geometry_field='mpoint', fields=('username',)))
                        
#   return HttpResponse(serialize('geojson', Gpslocation.objects.all(), geometry_field='mpoint', fields=('username',)))

# alternate queries - get last points for each distinct phone phonenumber
# Gpslocation.objects.order_by('phonenumber','gpstime').reverse().distinct('phonenumber')
# get last points for each distinct sessionid
# Gpslocation.objects.order_by('sessionid','gpstime').reverse().distinct('sessionid')

# Track serializer
def geojsonTrack(request):
    last_session = Gpslocation.objects.latest('gpstime').sessionid
    session = Gpslocation.objects.filter(sessionid__startswith=last_session).order_by('-gpstime')
#    session=Gpslocation.objects.order_by('sessionid','-gpstime').distinct('sessionid')
    line=LineString([s.mpoint for s in session])
    return HttpResponse(line.geojson)
