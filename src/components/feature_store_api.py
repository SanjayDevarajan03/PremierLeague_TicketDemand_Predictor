import os
from dotenv import load_dotenv
from src.components.feature_store_api import FeatureGroupConfig, FeatureViewConfig
from src.paths import PARENT_DIR

# load key-value pairs from .env file located in parent directory
load_dotenv(PARENT_DIR/'.env')

try:
    HOPSWORKS_PROJECT_NAME = os.environ['HOPSWORKS_PROJECT_NAME']
    HOPSWORKS_API_KEY = os.environ["HOPSWORKS_API_KEY"]
except:
    raise Exception(
        "Create an .env file on the project root with the HOPSWORKS_PROJECT_NAME and HOPSWORKS_API_KEY"
    )

FEATURE_GROUP_METADATA = FeatureGroupConfig(
    name = '',
    version=0,
    description='',
    primary_key=['sub_region_code', 'date'],
    event_time = 'date',
    online_enabled=True
)

FEATURE_VIEW_METADATA = FeatureViewConfig(
    name='',
    version=0,
    feature_group=FEATURE_GROUP_METADATA
)

MODEL_NAME = ''
MODEL_VERSION = 0

FEATURE_GROUP_MODEL_PREDICTIONS =  ''
FEATURE_GROUP_PREDICTIONS_METADATA = FeatureGroupConfig(
    name='',
    version='',
    description = 'Predictions generate by our production model',
    primary_key = ['sub_region_code', 'date'],
    event_time = 'date'
)

FEATURE_VIEW_PREDICTIONS_METADATA = FeatureViewConfig(
    name = '',
    version = 0,
    feature_group = FEATURE_GROUP_PREDICTIONS_METADATA
)

MONITORING_FV_NAME = 'monitoring_feature_view5'
MONITORING_FV_VERISON = ''
