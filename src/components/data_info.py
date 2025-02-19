import requests
import json
import pandas as pd
from datetime import datetime, timedelta
import requests_cache
from retry_requests import retry
import openmeteo_requests
from src.paths import *
from typing import Optional
from sklearn.prepreprocessing import LabelEncoder
import numpy as np
import tqdm
from datetime import datetime
from typing import Tuple



def download_and_extract_weather_data(start_date, end_date):
    cache_session = requests_cache.CachedSession('.cache', expire_after=1)
    retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
    openmeteo = openmeteo_requests.Client(session=retry_session)

    # Setup the Open-Meteo API client
    cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
    retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
    openmeteo = openmeteo_requests.Client(session=retry_session)

    # Make sure all required weather variables are listed here
    # The order of variables in hourly or daily is important to assign them correctly below
    url = "https://historical-forecast-api.open-meteo.com/v1/forecast"
    params = {
        "latitude": 52.52,
        "longitude": 13.41,
        "start_date": start_date,
        "end_date": end_date,
        "hourly": ["temperature_2m", "precipitation", "visibility"],
        "timeformat": "unixtime",
        "timezone": "Europe/London" 
    }

    try:
        # Feth data from the Open-Meteo API
        responses = openmeteo.weather_api(url, params=params)[0] # assuming single location

        # Process metadata
        print(f"Coordinates: {responses.Latitude()}°N {responses.Longitude()}°E")
        print(f"Elevation {responses.Elevation()} m asl")
        print(f"Timezone {responses.Timezone()} {responses.TimezoneAbbreviation()}")
        print(f"Timezone difference to GMT+0 {responses.UtcOffsetSeconds()} seconds")
        
        # Process hourly data. Te order of variables needs to be the same as requested.
        hourly = responses.hourly()
        hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()
        hourly_precipitation = hourly.Variables(1).ValuesAsNumpy()
        hourly_visibility = hourly.Variables(2).ValuesAsNumpy()

        hourly_data = {"date": pd.date_range(
            start=pd.to_datetime(hourly.Time(), unit="s", utc="True"),
            end = pd.to_datetime(hourly.TimeEnd(), unit = "s", utc="True"),
            freq = pd.Timedelta(seconds=hourly.Interval()),
            inclusive="left"
        )}

        hourly_data["temperature_2m"] = hourly_temperature_2m
        hourly_data["precipitation"] = hourly_precipitation
        hourly_data["visibility"] = hourly_visibility

        # Convert to DataFrame and process timestamps
        hourly_dataframe  = pd.DataFrame(data=hourly_data)

        hourly_dataframe["date"] = pd.to_datetime(hourly_dataframe["date"]).dt.floor("h").dt.tz_localize(None)

        # Save to file
        start_date_str = start_date.strftime('%Y-%m-%d')
        end_date_str = end_date.strftime('%Y-%m-%d')
        file_path = RAW_DATA_weather_DIR/f"weather_data_{start_date_str}_to{end_date_str}.csv"
        hourly_dataframe.to_csv(file_path, index=False)
        print(f"Weather data to saved to {file_path}")

        return hourly_dataframe
    except Exception as e:
        print(f"Error downloading weather data : {e}")
        return pd.DataFrame()
    

def load_full_data(start_date, end_date):
    df1 = download_and_extract_weather_data(start_date, end_date)
    full_date = pd.merge(df1,on="date", how="inner" )
    return full_date

def get_cutoff_indices_features_and_target(
    data: pd.DataFrame,
    input_seq_len: int,
    step_size: int
    ) -> list:
    stop_position = 1

    # Start the first sub-sequence at index position 0
    subseq_first_idx = 0
    subseq_mid_idx = input_seq_len
    subseq_last_idx = input_seq_len + 1
    indices = []

    while subseq_last_idx <= stop_position:
        indices.append((subseq_first_idx, subseq_mid_idx, subseq_last_idx))
        subseq_first_idx += step_size
        subseq_mid_idx += step_size
        subseq_last_idx += step_size
    return indices


def transform_ts_data_into_features_and_target(
        ts_data: pd.DataFrame,
        input_seq_len: int,
        step_size: int):
    """
    Slices and transposes data from time-series format into a (features, target)
    """
    