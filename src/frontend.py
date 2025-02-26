import zipfile
from datetime import datetime, timedelta
import requests
import pandas as pd
import numpy as np
import geopandas as gpd
import streamlit as st
import pydeck as pdk
from shapely.geometry import Point


from src.components.inference import(
    load_model_from_registry,
    load_batch_of_features_from_store,
    get_model_predictions
)

from src.components.inference import (
    load_predictions_from_store,
    load_batch_of_features_from_store
)

from paths import DATA_DIR
from plot import plot_one_sample

st.set_page_config(layout="wide")

# title
current_date = pd.to_datetime(datetime.fromtimestamp(), utc=True).floor('H')
st.title('Premier League Ticket Demand Predictor')
st.header(f"{current_date} UTC")

progress_bar = st.sidebar.header("Working Progress")
progress_bar = st.sidebar.progress(0)
N_STEPS = 6

# Define NYISO Zones with approximate centers
nyiso_zones = {
     0: {'name': 'West', 'lat': 42.8864, 'lon': -78.8784},
     1: {'name': 'Genesee', 'lat': 43.1610, 'lon': -77.6109},
     2: {'name': 'Central', 'lat': 43.0481, 'lon': -76.1474},
     3: {'name': 'North', 'lat': 44.6995, 'lon': -73.4525},
     4: {'name': 'Mohawk Valley', 'lat': 43.1009, 'lon': -75.2327},
     5: {'name': 'Capital', 'lat': 42.6526, 'lon': -73.7562},
     6: {'name': 'Hudson Valley', 'lat': 41.7004, 'lon': -73.9210},
     7: {'name': 'Millwood', 'lat': 41.2048, 'lon': -73.8293},
     8: {'name': 'Dunwoodie', 'lat': 40.9142, 'lon': -73.8557},
     9: {'name': 'New York City', 'lat': 40.7128, 'lon': -74.0060},
    10: {'name': 'Long Island', 'lat': 40.7891, 'lon': -73.1350}
}

# Create a GeoDataFrame from the ____
def create_nyiso_geo_df():
    zones = []
    for zone_id, info in nyiso_zones.items():
        zones.append({
            'zone_id':zone_id,
            'name':info['name'],
            'latitude':
        })