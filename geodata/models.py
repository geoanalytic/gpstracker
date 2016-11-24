# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import
from django.utils.encoding import python_2_unicode_compatible
from django.contrib.gis.db import models

# A simple point location with a name
@python_2_unicode_compatible
class Location(models.Model):
    name = models.CharField(max_length=50, default = 'Unknown location')
    mpoint = models.PointField()

    def __str__(self):
        return self.name
