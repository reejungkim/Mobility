# -*- coding: utf-8 -*-
# Copyright 2018-2019 Streamlit Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""An example of showing geographic data."""

import streamlit as st
from multiapp import MultiApp
import moving # import your app modules here

app = MultiApp()

import pydeck as pdk
#import matplotlib.pyplot as plt
#import seaborn as sns

import pandas as pd
import numpy as np
import altair as alt

import os
import time
import base64
import datetime as dt
import calendar 



from dotenv import load_dotenv
# .env file to environment
#load_dotenv()
load_dotenv(verbose=True)
token = os.getenv('MAPBOX_API_KEY')

# SETTING PAGE CONFIG TO WIDE MODE
st.set_page_config(layout='wide')


# LOADING DATA
DATE_TIME = "date/time"
DATA_URL = "http://s3-us-west-2.amazonaws.com/streamlit-demo-data/uber-raw-data-sep14.csv.gz"
#COMMUTE_DATA_URL = "https://raw.githubusercontent.com/ajduberstein/sf_public_data/master/bay_area_commute_routes.csv"


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
    data[DATE_TIME] = pd.to_datetime(data[DATE_TIME])
    return data

# LINK FOR DOWNLOADING DATA
st.markdown(get_table_download_link(load_data(100000)), unsafe_allow_html=True)

data = load_data(100000)

# FEATURE ENGINEERING
data['date/time']=  pd.to_datetime(data['date/time'])
data['year'] = data['date/time'].dt.year
data['month'] = data['date/time'].dt.month
data['day'] = data['date/time'].dt.day
data['hour'] = data['date/time'].dt.hour
data['dayofweek'] =  data['date/time'].dt.strftime('%a') 
#data['dayofweek_encoded'] = data['date/time'].dt.dayofweek # dayofweek


# CREATING FUNCTION FOR MAPS

def map(data, lat, lon, zoom):
    layer = pdk.Layer(
        'HexagonLayer', #'HeatmapLayer',
        data,
        get_position='[lon, lat]',
        radius = 120,
        auto_highlight=True,
        elevation_scale=4,
        pickable=True,
        elevation_range=[0, 1000],
        extruded=True,                 
        coverage=1)
    view_state = pdk.ViewState(
        latitude= lat,
        longitude= lon,
        zoom= zoom,
        pitch= 50
        ) 
    r = pdk.Deck(layers=[layer], initial_view_state=view_state)
    return r
    #st.write(r)



#LAYING OUT THE TOP SECTION OF THE APP
st.title("NYC Uber Ridesharing Data")
row1_1, row1_2, row1_3 = st.beta_columns((2,2,3))


with row1_1:
    hour_selected = st.slider("Select hour of pickup", 0, 23)
    data = data[data[DATE_TIME].dt.hour == hour_selected] 

with row1_2:
    dayofweek_selected  = st.multiselect('Select day(s) of week',   
                                         options= ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'], 
                                          default= ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat','Sun'])
    data = data[data['dayofweek'].isin(dayofweek_selected)]

with row1_3:
    st.write(
    """
    ##
    Examining how Uber pickups vary over time in New York City's and at its major regional airports.
    By sliding the slider on the left you can view different slices of time and explore different transportation trends.
    """)


# LAYING OUT THE MIDDLE SECTION OF THE APP WITH THE MAPS
row2_1, row2_2, row2_3, row2_4 = st.beta_columns((2,1,1,1))

# SETTING THE ZOOM LOCATIONS FOR THE AIRPORTS
la_guardia= [40.7900, -73.8700]
jfk = [40.6650, -73.7821]
newark = [40.7090, -74.1805]
zoom_level = 12
midpoint = (np.average(data["lat"]), np.average(data["lon"]))


with row2_1:
    st.write("**All New York City from %i:00 and %i:00**" % (hour_selected, (hour_selected + 1) % 24))
    st.write(map(data, midpoint[0], midpoint[1], 11))

with row2_2:
    st.write("**La Guardia Airport**")
    st.write(map(data, la_guardia[0],la_guardia[1], zoom_level))

with row2_3:
    st.write("**JFK Airport**")
    st.write(map(data, jfk[0],jfk[1], zoom_level))

with row2_4:
    st.write("**Newark Airport**")
    st.write(map(data, newark[0],newark[1], zoom_level))






# st.write("")

