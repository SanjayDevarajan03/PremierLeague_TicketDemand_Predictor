from typing import Optional, List
from dataclasses import dataclass
import hsfs
import hopsworks
import src.components.feature_group_config as config
from src.logger import get_logger

logger = get_logger()

@dataclass
class FeatureGroupConfig:
    name: str
    version: str
    description: str
    primary_key: List[str]
    event_time: str
    online_enabled: Optional[bool] = False

@dataclass
class FeatureViewConfig:
    name: str
    version: int
    feature_group: FeatureGroupConfig

def get_feature_store() -> hsfs.feature_store.FeatureStore:
    """
    Connects to Hopsworks and returns a pointer to the feature store

    Returns:
        hsfs.feature_store.FeatureStore: pointer to the feature store
    """
    project = hopsworks.login(
        project=config.HOPSWORKS_PROJECT_NAME,
        api_key_value = config.HOPSWORKS_API_KEY
    )
    return project.get_feature_store()

def get_or_create_feature_group(feature_group_metadata: FeatureGroupConfig) -> hsfs.feature_group.FeatureGroup:
    """
    Connects to the feature store and returns a pointer to the given feature group `name`

    Args:
        name(str): name of the feature group
        version (Optional[int], optional): _description_. Defaults to 1.

    Returns:
        hsfs.feature_group.FeatureGroup: pointer to the feature group
    """
    return get_feature_store().get_or_create_feature_group(
        name=feature_group_metadata.name,
        version=feature_group_metadata.version,
        description=feature_group_metadata.description,
        primary_key = feature_group_metadata.primary_key,
        event_time = feature_group_metadata.event_time,
        online_enabled = feature_group_metadata.online_enabled
    )
