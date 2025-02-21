from datetime import datetime, timedelta
import hopsworks
import pandas as pd
import numpy as np

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