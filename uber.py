#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 28 00:20:50 2020

@author: reejungkim
"""

import os
from dotenv import load_dotenv
# .env file to environment
#load_dotenv()
load_dotenv(verbose=True)
token = os.getenv('MAPBOX_API_KEY')

import pydeck as pdk
import streamlit as st


# 2014 locations of car accidents in the UK
UK_ACCIDENTS_DATA = ('https://raw.githubusercontent.com/uber-common/deck.gl-data/master/examples/3d-heatmap/heatmap-data.csv')

# Define a layer to display on a map
layer = pdk.Layer(
    'HexagonLayer',
    UK_ACCIDENTS_DATA,
    get_position='[lng, lat]',
    auto_highlight=True,
    elevation_scale=50,
    pickable=True,
    elevation_range=[0, 3000],
    extruded=True,                 
    coverage=1)

# Set the viewport location
view_state = pdk.ViewState(
    longitude=-1.415,
    latitude=52.2323,
    zoom=6,
    min_zoom=5,
    max_zoom=15,
    pitch=40.5,
    bearing=-27.36)

# Combined all of it and render a viewport
r = pdk.Deck(
    map_style="mapbox://styles/mapbox/light-v9",
    layers=[layer],
    initial_view_state=view_state,
    tooltip={"html": "<b>Elevation Value:</b> {elevationValue}", "style": {"color": "white"}})

#r = pydeck.Deck(layers=[layer], initial_view_state=view_state)

#st.write(pydeck.Deck(layers=[layer], initial_view_state=view_state))

st.pydeck_chart(r)
# Render

#r.to_html('demo_layer.html')

# Please see the note about using a Mapbox API token here:
# https://github.com/uber/deck.gl/tree/master/bindings/python/pydeck#mapbox-api-token