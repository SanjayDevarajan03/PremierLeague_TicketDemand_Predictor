from typing import Optional, List
from datetime import timedelta
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

def plot_one_sample(
        features: pd.DataFrame,
        targets: pd.DataFrame,
        example_id: int,
        predictions: Optional[pd.DataFrame] = None,
    ):

    features_ = features.iloc[example_id]

    if targets is not None:
        target_ = targets.iloc[example_id]
    else:
        target_ = None

    
