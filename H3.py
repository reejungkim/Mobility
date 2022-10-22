#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan  4 17:25:13 2021

@author: reejungkim
"""

import os
import pandas as pd
import numpy as np

from dotenv import load_dotenv
load_dotenv(verbose=True)
token = os.getenv('MAPBOX_API_KEY')

import pydeck as pdk

from h3 import h3
#h3_key = h3.geo_to_h3(latitude, longitude, level)
#h3.h3_to_geo_boundary(h3_address=h3_key)

# h3_address = h3.geo_to_h3(37.3615593, -122.0553238, 5)
# hex_center_coordinates = h3.h3_to_geo(h3_address)
# boundary = h3.h3_to_geo_boundary(h3_address)

# 2014 locations of car accidents in the UK
UK_ACCIDENTS_DATA = ('https://raw.githubusercontent.com/uber-common/deck.gl-data/master/examples/3d-heatmap/heatmap-data.csv')
data = pd.read_csv(UK_ACCIDENTS_DATA)

def lat_lng_to_h3(row):
    return h3.geo_to_h3(row['lat'], row['lng'], 11)

def hex_center(row):
    return h3.h3_to_geo_boundary(row['h3_key'])

data['h3_key'] = data.apply(lat_lng_to_h3, axis=1)
#data['boundary'] = data.apply(hex_center, axis=1)


def map(data, lat, lon, zoom):
    layer= pdk.Layer(
        "HexagonLayer",
        data=data,
        get_position='[lng, lat]',
        radius=100,
        elevation_scale=4,
        elevation_range=[0, 1000],
        pickable=True,
        extruded=True,
        )
    view_state = pdk.ViewState(
        latitude= lat,
        longitude= lon,
        zoom= zoom,
        pitch= 50
        ) 
    r = pdk.Deck(
        map_style="mapbox://styles/mapbox/light-v9",
        layers=[layer], 
        initial_view_state=view_state
        )
    r.to_html('r.html')


zoom_level = 12
midpoint = (np.average(data["lat"]), np.average(data["lng"]))
map(data, midpoint[0], midpoint[1], 11)





