from test_plus.test import TestCase
from .models import Location
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
