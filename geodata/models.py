# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import
from datetime import datetime
import pytz
from django.utils.encoding import python_2_unicode_compatible
from django.contrib.gis.db import models
from cookie_cutter_demo.users.models import User

# A simple point location with a name
@python_2_unicode_compatible
class Location(models.Model):
    name = models.CharField(max_length=50, default = 'Unknown location')
    mpoint = models.PointField()

    def __str__(self):
        return self.name

# A gps tracker message
@python_2_unicode_compatible
class Gpslocation(models.Model):
    lastupdate=models.DateTimeField(auto_now_add=True)
    latitude = models.FloatField(default=0.000000)
    longitude = models.FloatField(default=0.000000)
    speed = models.IntegerField(default=0)
    direction = models.IntegerField(default=0)
    distance = models.FloatField(default=0.000000)
    gpstime = models.DateTimeField(default=datetime(2001,1,1,1,1,1,tzinfo=pytz.utc),blank=True)
    locationmethod = models.CharField(max_length=50, default='',blank=True)
    username = models.CharField(max_length=50, default='',blank=True)
    phonenumber = models.CharField(max_length=50, default='',blank=True)
    device_id = models.ForeignKey("Device")
    sessionid = models.CharField(max_length=50, default='',blank=True)
    accuracy = models.IntegerField(default=0)
    extrainfo = models.CharField(max_length=255, default='',blank=True)
    eventtype = models.CharField(max_length=50, default='',blank=True)
    
    # GeoDjango-specific: a geometry field (MultiPolygonField)
    mpoint = models.PointField()
    
    class Meta:
        verbose_name_plural = "Gps Locations"

    # Returns the string representation of the model.
    def __str__(self):              # __unicode__ on Python 2
        return ' '.join([self.username,self.gpstime.strftime('%Y-%m-%d %H:%M')])

# A table to link devices to users
@python_2_unicode_compatible
class Device(models.Model):
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True,null=True)
    phonenumber = models.CharField(max_length=50)
    
    class Meta:
      unique_together=("owner", "phonenumber")
    
    def __str__(self):    # __unicode__ on Python 2
        if(self.owner is None):
            return ' '.join(['No Owner', self.phonenumber])
        else:
            return ' '.join([self.owner.username, self.phonenumber])
    
