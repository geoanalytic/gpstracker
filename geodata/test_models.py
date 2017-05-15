from test_plus.test import TestCase
from datetime import datetime
from .models import Location, Gpslocation
from django.contrib.gis.geos import Point

# Tests for geodata classes

class LocationModelTest(TestCase):

    def test_saving_and_retrieving_locations(self):
        first_point = Location()
        first_point.name = "The first point"
        first_point.mpoint = Point(-112.54, 68.9)
        first_point.save()

        second_point = Location()
        second_point.name = "The second point"
        second_point.mpoint = Point(149.36, -10.52)
        second_point.save() 

        saved_points = Location.objects.all()
        self.assertEqual(saved_points.count(), 2)

        first_saved_point = saved_points[0]
        self.assertEqual(first_saved_point.name, "The first point" )
        self.assertEqual(first_saved_point.mpoint.x, -112.54)
        self.assertEqual(first_saved_point.mpoint.y, 68.9)

        second_saved_point = saved_points[1]
        self.assertEqual(second_saved_point.name, "The second point" )
        self.assertEqual(second_saved_point.mpoint.x, 149.36)
        self.assertEqual(second_saved_point.mpoint.y, -10.52)

class GpslocationModelTest(TestCase):

    def test_saving_and_retrieving_gpslocations(self):  
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

        first_saved_point = saved_points[0]
        self.assertEqual(first_saved_point.phonenumber, 'Test-0585-555-9090' )
        self.assertEqual(first_saved_point.mpoint.x, -112.54)
        self.assertEqual(first_saved_point.mpoint.y, 52.1)

        second_saved_point = saved_points[1]
        self.assertEqual(second_saved_point.sessionid, '5cb5b39-3583-42d8-9106-dddebede5aef' )
        self.assertEqual(second_saved_point.mpoint.x, second_saved_point.longitude)
        self.assertEqual(second_saved_point.mpoint.y, second_saved_point.latitude)        

# "GET /geodata/tracker/?date=2017-05-03%2B15%253A26%253A33&distance=0.0&latitude=51.1086728&phonenumber=ead0a898-5338-4486-b626-d8e9a470d18c&accuracy=49&sessionid=d5cb5b39-3583-42d8-9106-dddebede5aef&speed=0&extrainfo=0&eventtype=android&locationmethod=fused&longitude=-114.1860708&username=Dave&direction=0 HTTP/1.0""
