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
from django.contrib.gis.db.models.aggregates import MakeLine
from django.db.models.aggregates import Min

from .models import Location, Gpslocation, Device
from .forms import Gpslocationform

# Geojson serializer for Locations
def geojsonFeedLocation(request):
    return HttpResponse(serialize('geojson', Location.objects.all(),fields=('name','mpoint')))

# Views relating to Gps Tracker locations
# A track request should include a valid coordinate plus some optional data
# Currently this function will throw an error because the timestamp does not specify a timezone 
# use a logger for debugging the messages
logger = logging.getLogger(__name__)

def track(request):
    logger.info('Got tracking request')
    if request.method == 'GET':
        track_data = Gpslocationform(request.GET)
        if track_data.is_valid():
            track_point = track_data.save(commit=False)
            # create a GEOS point feature from the reported coordinates
            track_point.mpoint = Point(track_data.cleaned_data['longitude'], track_data.cleaned_data['latitude'])
            # currently getting naive timestamps, which will be converted to fake UTC using the timezone of the server
            # how to fix this?  Really should modify the phone app
            track_point.gpstime = datetime.strptime(unquote(track_data.cleaned_data['date']),'%Y-%m-%d+%H:%M:%S')
            # get or create the device_id key
            track_point.device_id, created = Device.objects.get_or_create(phonenumber = track_data.cleaned_data['phonenumber'])
            track_point.save()
        else:
            logger.error('Failed to validate track data')
    else:
        logger.error('Not a GET request')

    # this function never returns anything (maybe there should be a debug statement)
    return HttpResponse('')

# Geojson serializer
def geojsonFeed(request):
    if request.user.is_authenticated:
        return HttpResponse(serialize('geojson', 
                        Gpslocation.objects.filter(device_id__owner = request.user).order_by('phonenumber','-gpstime').distinct('phonenumber'), 
                        geometry_field='mpoint', fields=('username','device_id',)))
    else:
        return HttpResponse(serialize('geojson',Location.objects.all(), geometry_field='mpoint'))
                        
#   return HttpResponse(serialize('geojson', Gpslocation.objects.all(), geometry_field='mpoint', fields=('username',)))

# alternate queries - get last points for each distinct phone phonenumber
# Gpslocation.objects.order_by('phonenumber','gpstime').reverse().distinct('phonenumber')
# get last points for each distinct sessionid
# Gpslocation.objects.order_by('sessionid','gpstime').reverse().distinct('sessionid')

# Track serializer
def geojsonTrack(request):
    if request.user.is_authenticated:    
        last_session = Gpslocation.objects.filter(device_id__owner = request.user).latest('gpstime').sessionid
        if last_session:
            session = Gpslocation.objects.filter(device_id__owner = request.user).filter(sessionid__exact=last_session).order_by('-gpstime')

            if session:
                device = session[0].device_id.id
                srid = session[0].mpoint.srs.srid
                if(session.count() >= 2):
                    line=LineString([s.mpoint for s in session])
                else:
                    line=LineString([session[0].mpoint, session[0].mpoint])
                
                linelist=[]
                linelist.append('{ "type": "Feature", "properties": {"id":"%(id)s"},"geometry":%(linestr)s' % {"id":device,"linestr":line.geojson})
                result = '{"type": "FeatureCollection",  "features": [' + ",".join(linelist) + '}]}'
                return HttpResponse(result)
    else:
        return HttpResponse('')
        

def geojsonTrack2(request):        
    last_session = Gpslocation.objects.latest('gpstime').sessionid
    if last_session:
        session_line = Gpslocation.objects.filter(sessionid__startswith=last_session).aggregate(MakeLine('mpoint'),id=Min('device_id'))
        return HttpResponse(serialize('geojson', session_line, fields=('username','id',)))
    else:
        return HttpResponse('')    
