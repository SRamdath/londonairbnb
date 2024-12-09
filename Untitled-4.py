#!/usr/bin/env python
# coding: utf-8

# In[1]:


import streamlit as st
import pandas as pd
from geopy.distance import geodesic

# Load dataset
try:
    listings = pd.read_csv('data/processed_listings.csv')
    st.write("Dataset loaded successfully!")
    st.write(listings.head())  # Display the dataset to verify
except FileNotFoundError:
    st.error("The file 'processed_listings.csv' was not found. Please ensure it is in the 'data' folder.")
    st.stop()

# Process room type columns
room_type_columns = [col for col in listings.columns if col.startswith("room_type_")]
listings['room_type'] = listings[room_type_columns].idxmax(axis=1).str.replace("room_type_", "")

# User input: Max distance and room type
max_distance = st.slider("Maximum Distance from Venue (km)", 1.0, 20.0, 5.0)
selected_room_type = st.selectbox("Room Type", listings['room_type'].unique())

# Define the tournament location
tournament_location = (51.509865, -0.118092)  # Example coordinates for central London

# Calculate distance from the venue
listings['distance_from_venue'] = listings.apply(
    lambda x: geodesic((x['latitude'], x['longitude']), tournament_location).km, axis=1
)

# Filter the listings
filtered_listings = listings[
    (listings['distance_from_venue'] <= max_distance) &
    (listings['room_type'] == selected_room_type)
]

# Display results
st.write(f"Filtered {len(filtered_listings)} listings close to the tournament venue.")
st.write(filtered_listings)


# In[ ]:



