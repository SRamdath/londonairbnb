import streamlit as st
import pandas as pd
from geopy.distance import geodesic

# Load dataset
try:
    listings = pd.read_csv('data/processed_listings.csv')
    st.write("Data successfully loaded.")
except FileNotFoundError:
    st.error("Error: The file 'processed_listings.csv' is not found. Please ensure the file exists in the 'data' folder.")
    st.stop()
except Exception as e:
    st.error(f"An unexpected error occurred: {e}")
    st.stop()

# Tournament location: Olympia London
tournament_location = (51.4952, -0.2103)  # Latitude and Longitude for Olympia London

# Add a toggle for distance unit
distance_unit = st.radio("Select Distance Unit", options=["Kilometers (km)", "Miles"])

# Adjust distance calculation based on unit
listings['distance_from_venue'] = listings.apply(
    lambda x: geodesic((x['latitude'], x['longitude']), tournament_location).km
    if distance_unit == "Kilometers (km)"
    else geodesic((x['latitude'], x['longitude']), tournament_location).miles,
    axis=1
)

# User input: Distance, room type, price range, number of reviews
max_distance = st.slider(f"Maximum Distance from Venue ({distance_unit})", 1.0, 20.0, 5.0)
room_type_columns = [col for col in listings.columns if col.startswith("room_type_")]
room_type_options = [col.replace("room_type_", "").replace("_", " ").title() for col in room_type_columns]
selected_room_type = st.selectbox("Room Type", room_type_options)

min_price, max_price = st.slider("Price Range ($)", int(listings['price'].min()), int(listings['price'].max()), (50, 300))
min_reviews = st.slider("Minimum Number of Reviews", 0, int(listings['number_of_reviews'].max()), 0)

# Filter dataset based on user input
selected_room_type_col = f"room_type_{selected_room_type.replace(' ', '_').lower()}"
if selected_room_type_col in listings.columns:
    filtered_listings = listings[
        (listings['distance_from_venue'] <= max_distance) &
        (listings[selected_room_type_col] == 1) &
        (listings['price'] >= min_price) &
        (listings['price'] <= max_price) &
        (listings['number_of_reviews'] >= min_reviews)
    ]
else:
    st.error(f"Error: Room type '{selected_room_type}' is not available in the dataset.")
    filtered_listings = pd.DataFrame()

# Display filtered listings
if not filtered_listings.empty:
    st.write(f"Filtered {len(filtered_listings)} listings close to the tournament venue.")
    st.dataframe(filtered_listings[['id', 'name', 'host_id', 'host_name', 'neighbourhood', 'price', 'distance_from_venue']])
    st.map(filtered_listings[['latitude', 'longitude']])
else:
    st.write("No listings found matching the selected criteria.")

# Show summary statistics
if not filtered_listings.empty:
    st.subheader("Summary Statistics")
    st.write(f"Average Price: ${filtered_listings['price'].mean():.2f}")
    st.write(f"Minimum Price: ${filtered_listings['price'].min():.2f}")
    st.write(f"Maximum Price: ${filtered_listings['price'].max():.2f}")



