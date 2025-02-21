import os
from datetime import date, timedelta
from pathlib import Path
from typing import Optional, Tuple

import numpy as np
import pandas as pd
import optuna
from comet_ml import Experiment
from dotenv import load_dotenv
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import KFold

from src.components.feature_group_config import FEATURE_VIEW_METADATA, N_HYPERPARAMETER_SEARCH_TRIALS
import src.components.feature_group_config as config
from src.components.data_info import transform_ts_data_into_features_and_target, train_test_split
from src.components.feature_store_api import get_or_create_feature_view
from src.logger import get_logger
from src.components.model_info import get_pipeline
from src.components.model_registry_api import push_model_to_registry
from src.paths import DATA_CACHE_DIR, PARENT_DIR

logger = get_logger()

# load variables from.env file as environment variables
load_dotenv(PARENT_DIR / '.env')

def fetch_features_and_targets_from_store(
        from_date: pd.Timestamp,
        to_date: pd.Timestamp,
        step_size: int,        
) -> pd.DateFrame:
    """
    Fetches time-series data from the store, transforms it into features and 
    targets and returns it as a pandas dataframe.
    """
    # get pointer to feature view
    logger.info("Getting pointer to feature view...")
    feature_view = get_or_create_feature_view(FEATURE_VIEW_METADATA)

    # generate training data from the feature view
    logger.info("Generating training data")
    ts_data, _ = feature_view.training_data(description="Time-series hourly taxi rides")

    # filter data based on the from_date and to_date expressed\
    # as Unix milliseconds
    from_ts = int(from_date.timestamp()*1000)
    

