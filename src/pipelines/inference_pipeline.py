from argparse import ArgumentParser
from datetime import datetime
from typing import Optional

import pandas as pd
from hsfs.client.exceptions import RestAPIError
from retry import retry

from src.components.feature_group_config import FEATURE_GROUP_PREDICTIONS_METADATA, MODEL_NAME
from src.components.feature_store_api import get_or_create_feature_group
from src.components.inference import get_model_predictions, load_batch_of_features_from_store
from src.logger import get_logger
from src.components.model_registry_api import get_latest_model_from_registry

logger = get_logger()

@retry(RestAPIError, tries=3, delay=60)
def save_predictions_to_feature_store(predcitions: pd.DataFrame) -> None:
    """
    Saves model predictions to the feature store.

    We add retry to this function because sometimes the feature store API fials, beacuase of too many concurrent jobs.
    """

    logger.info('Getting pointer to the feature group for model predictions')
    feature_group = get_or_create_feature_group(FEATURE_GROUP_PREDICTIONS_METADATA)

    try:
        logger.info('Saving predictions to the feature store')
        feature_group.insert(predcitions, write_options={'wait_for_job': False})
    except RestAPIError as e:
        logger.info('Failed to save predictions to the feature store')
        logger.info('Retrying in 60 seconds...')
        raise e