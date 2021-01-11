#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan  7 17:32:24 2021

@author: reejungkim
"""


import streamlit as st
import pydeck as pdk

import pandas as pd
import numpy as np
import altair as alt

import os
import time
import base64
import datetime as dt
import calendar 

# from geopy.geocoders import Nominatim 
# geolocator = Nominatim(user_agent="n/a")


from dotenv import load_dotenv
# .env file to environment
#load_dotenv()
load_dotenv(verbose=True)
token = os.getenv('MAPBOX_API_KEY')


# SETTING PAGE CONFIG TO WIDE MODE
st.set_page_config(layout='wide')


# LOADING DATA
DATA_URL = "https://raw.githubusercontent.com/ajduberstein/sf_public_data/master/bay_area_commute_routes.csv"

def get_table_download_link(df):
    """Generates a link allowing the data in a given panda dataframe to be downloaded
    in:  dataframe
    out: href string
    """
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # some strings <-> bytes conversions necessary here
    href = f'<a href="data:file/csv;base64,{b64}" download="myfilename.csv">Download data</a>'
    return href

@st.cache(allow_output_mutation=True, persist=True)
#@st.cache(persist=True)
def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis="columns", inplace=True)
    return data

# def getAddress(lat, lng):
#     latlng = str(lat) +','+ str(lng)
#     location = geolocator.reverse(latlng)
#     return location.address

# LINK FOR DOWNLOADING DATA
st.markdown(get_table_download_link(load_data(1000)), unsafe_allow_html=True)

df = load_data(1000)
# df['from'] = df.apply(lambda x: getAddress(x.lat_w, x.lng_w), axis=1)


# MAP
GREEN_RGB = [0, 255, 0, 40]
RED_RGB = [240, 100, 0, 40]

# Specify a deck.gl ArcLayer
arc_layer = pdk.Layer(
    "ArcLayer",
    data=df,
    get_width="S000 * 2",
    get_source_position=["lng_h", "lat_h"],
    get_target_position=["lng_w", "lat_w"],
    get_tilt=15,
    get_source_color=RED_RGB,
    get_target_color=GREEN_RGB,
    pickable=True,
    auto_highlight=True,
)

view_state = pdk.ViewState(
    latitude=37.7576171,
    longitude=-122.5776844,
    bearing=45,
    pitch=50,
    zoom=8,
)

TOOLTIP_TEXT = {"html": "({lng_h}, {lat_h}) to ({lng_w}, {lat_w})" } #" Home of commuter in red; work location in green"}


r = pdk.Deck(arc_layer, 
             initial_view_state=view_state, 
             tooltip=TOOLTIP_TEXT,
            map_style = "mapbox://styles/mapbox/streets-v11")


st.write(r)


