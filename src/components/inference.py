from datetime import datetime, timedelta
import hopsworks
import pandas as pd
import numpy as np
import joblib
from pathlib import Path

import src.components.feature_group_config as config
from src.components.feature_store_api import get_feature_store, get_or_create_feature_view
from src.components.feature_group_config import FEATURE_VIEW_METADATA

def get_hopsworks_project() -> hopsworks.project.Project:
    return hopsworks.login(
        project=config.HOPSWORKS_PROJECT_NAME,
        api_key_value=config.HOPSWORKS_API_KEY
    )

def get_model_predictions(model, features: pd.DataFrame) -> pd.DataFrame:
    """Generate model predictions based on input features."""
    assert features.shape[0] > 0, "Make sure your feature pipeline is up and running"

    predictions = model.predict(features)

    results = pd.DataFrame()
    results['predicted_demand'] = predictions.round(0)

    return results # Ensure the function returns the DataFrame

def load_batch_of_features_from_store(current_date: pd.Timestamp) -> pd.DataFrame:
    """Features the batch of features used by the ML system at `current_date`
    Args:
        current_date (datetime): datetime of the prediction for which we want
        to get the batch of features

    Returns:
        pd.DataFrame: 4 columns:
            - `date`
            - `demand`
            - `temperature`
            - `precipitation`
            - `visibility`
    """

    n_features = config.N_FEATURES
    feature_view = get_or_create_feature_view(FEATURE_VIEW_METADATA)

    # Define time range
    fetch_date_to = pd.to_datetime(current_date - timedelta(hours=1), utc=True)
    fetch_date_from = pd.to_datetime(current_date - timedelta(days=28), utc=True)

    # Fetch data
    ts_data = feature_view.get_batch_data(
        start_time = fetch_date_from - timedelta(days=1),
        end_time = fetch_date_to + timedelta(days=1)
    )

    print('Dates before filtering:')
    print(ts_data['date'].min(), ts_data['date'].max())

    # Convert timestamps to milliseconds
    ts_from = int(fetch_date_from.timestamp()*1000)
    ts_to = int(fetch_date_to.timestamp() * 1000)
    
    # Filter the data for the required time period
    ts_data = ts_data.groupby('sub_region_code').tail(672)
    print(ts_data.groupby('sub_region_code').tail(10))
    print('Dates after filtering:')
    print(ts_data['date'].min(), ts_data['date'].max())

    # Sort data by location and time
    ts_data.sort_values(by=['sub_region_code', 'date'], inplace=True)

    # Count records per sub-region
    location_counts = ts_data.groupby('sub_region_code').size()

    # Identify valid sub-regions that meet the required record count
    valid_sub_regions = location_counts[location_counts==config.N_FEATURES].index
    print(valid_sub_regions)

    # Filter the dataset to retain only valid sub-regions
    ts_data = ts_data[ts_data['sub_region_code'].isin(valid_sub_regions)]

    print(f"Filtered out sub-regions that do not meet the required {config.N_FEATURES} records.")

    # Transpose time-series data into a feature for each `sub_region_code`.
    location_ids = ts_data['sub_region_code'].unique()
    x = np.ndarray(shape=(len(location_ids), n_features), dtype = np.float32)

    temperature_values = []
    for i, location_id in enumerate(location_ids):
        ts_data_i = ts_data.loc[ts_data.sub_region_code == location_id, :]
        ts_data_i = ts_data_i.sort_values(by=['date'])
        x[i, :] = ts_data_i['demand'].values
        temperature_values.append(ts_data_i['temperature_2m'].iloc[-1])


    # Convert numpy arrays to Pandas dataframe
    features = pd.DataFrame(
        x, columns = [f'demand_previous_{i+1}_hour' for i in reversed(range(n_features))]
    )

    features['tempreature_2m'] = temperature_values
    features['date'] = current_date
    features['sub_region_code'] = location_ids
    features.sort_values(by=['sub_region_code'], inplace=True)



def load_model_from_registry():

    project = get_hopsworks_project()
    model_registry = project.get_model_registry()
    model = model_registry.get_model(
        name = config.MODEL_NAME,
        version = config.MODEL_VERSION
    )

    model_dir = model.download()
    model =joblib.load(Path(model_dir)/'LGB_model.pkl')