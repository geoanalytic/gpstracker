from test_plus.test import TestCase, RequestFactory
from django.test import Client
from .views import track, geojsonFeed, geojsonTrack
from datetime import datetime
from .models import Gpslocation
from django.contrib.gis.geos import Point

# Tests for geodata views
# submit a couple of points for testing
class TrackTest(TestCase):
    def setUpTestData(self):
        self.factory = RequestFactory()
        first_point = Gpslocation()
        first_point.latitude = 52.1
        first_point.longitude = -112.54
        first_point.speed = 5
        first_point.direction = 110
        first_point.gpstime = datetime.utcnow()
        first_point.username = 'Test'
        first_point.phonenumber = 'Test-0585-555-9090'
        first_point.sessionid = '5cb5b39-3583-42d8-9106-dddebede5aef'
        first_point.accuracy = 49
        first_point.mpoint = Point(-112.54, 52.1)
        first_point.save()
        
        second_point = Gpslocation()
        second_point.latitude = 55.1
        second_point.longitude = -114.54
        second_point.speed = 5
        second_point.direction = 110
        second_point.gpstime = datetime.utcnow()
        second_point.username = 'Test'
        second_point.phonenumber = 'Test-0585-555-9090'
        second_point.sessionid = '5cb5b39-3583-42d8-9106-dddebede5aef'
        second_point.accuracy = 4
        second_point.mpoint = Point(-114.54, 55.1)
        second_point.save()           
        
        saved_points = Gpslocation.objects.all()
        self.assertEqual(saved_points.count(), 2)            
       
    def test_addpoint(self):
        request = self.factory.get('/geodata/tracker', 
                  {'date':'2017-05-15+15:25:30','distance':0.0,
                  'latitude':51.1086728,
                  'phonenumber':'ead0a898-5338-4486-b626-d8e9a470d18c',
                  'accuracy':49,
                  'sessionid':'d5cb5b39-3583-42d8-9106-dddebede5aef',
                  'speed':0,'extrainfo':0,'eventtype':'android',
                  'locationmethod':'fused','longitude':-114.1860708,
                  'username':'Dave','direction':0})

        # Test Track() as if it were deployed at /geodata/tracker
        response = track(request)

        self.assertEqual(response.status_code, 200)
    
        request = self.factory.get('/geodata/tracker', 
                  {'date':'2017-05-15+15:26:30','distance':0.0,
                  'latitude':51.1086730,
                  'phonenumber':'ead0a898-5338-4486-b626-d8e9a470d18c',
                  'accuracy':42,
                  'sessionid':'d5cb5b39-3583-42d8-9106-dddebede5aef',
                  'speed':5,'extrainfo':0,'eventtype':'android',
                  'locationmethod':'fused','longitude':-114.1860800,
                  'username':'Dave','direction':180})

        # Test Track() as if it were deployed at /geodata/tracker
        response = track(request)

        self.assertEqual(response.status_code, 200)
        
    def test_status(self):
        response = self.get_check_200('/geodata/data.geojson')        
        
    def test_pointfeed(self):
        response = self.get('/geodata/data.geojson')
        print(response)
#        self.assertResponseContains('FeatureCollection')
        self.assertResponseContains('coordinates')
        
    def test_trackfeed(self):
        self.get('/geodata/track.geojson')
        self.assertResponseContains('LineString')
        self.assertResponseContains('coordinates')        
        
