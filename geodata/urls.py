# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^tracker/$',views.track,name='tracker'),             # for incoming gps tracker data
    url(r'^data.geojson$', views.geojsonFeed, name='data'),    # feed GPS points
    url(r'^track.geojson$', views.geojsonTrack, name='track'),  # feed GPS lines
    url(r'^track.geojson2$', views.geojsonTrack2, name='track2'),  # feed GPS lines    
    url(r'^locations.geojson$', views.geojsonFeedLocation, name='data'),    # feed Location points
]
