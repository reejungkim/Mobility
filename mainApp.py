#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb  5 00:15:01 2021

@author: reejungkim
"""

import streamlit as st
from multiapp import MultiApp
import moving, app # import your app modules here

app = MultiApp()

st.markdown("""
# Multi-Page App
This multi-page app is using the [streamlit-multiapps](https://github.com/upraneelnihar/streamlit-multiapps) framework developed by [Praneel Nihar](https://medium.com/@u.praneel.nihar). Also check out his [Medium article](https://medium.com/@u.praneel.nihar/building-multi-page-web-app-using-streamlit-7a40d55fa5b4).
""")

# Add all your application here
app.add_app("Home", app.app)
app.add_app("Commute data", moving.app)

# The main app
app.run()