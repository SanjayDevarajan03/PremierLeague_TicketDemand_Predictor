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

    
    ts_columns_features = [c for c in features.columns if c.startswith('demand_previous_')]
    ts_column_targets = [c for c in targets.columns if c.startswith('demand_next_')]
    ts_values_features = [features_[c] for c in ts_columns_features]
    ts_values_targets = [target_[c] for c in ts_column_targets]

    ts_dates_features = pd.date_range(
        features_['date'] - timedelta(hours=len(ts_columns_features)),
        freq = 'H'
    )

    ts_dates_targets = pd.date_range(
        features_['pickup_hour'],
        features_['pickup_hour'] + timedelta(hours=len(ts_column_targets)-1),
        freq='H'
    )

    fig =go.Figure()
    title = f"Pick up hour = {features_["pickup_hour"]}, location_id={features_["pickup_location_id"]}"
    fig = px.line(x=ts_dates_features, y=ts_values_features, template='plotly_dark', markers=True, title=title)


    targets_fig = px.line(x=ts_dates_targets, y =target_.values.tolist(),
            template='plotly_dark', markers=True, title='actual values')
    
    targets_fig.update_traces(line_color='green')
    fig.add_traces(targets_fig.data)

    if predictions is not None:
        prediction_ = predictions.iloc[example_id]
        prediction_fig = px.line(x=ts_dates_targets, y = prediction_.values.tolist(),
                                template='plotly_dark')
        prediction_fig.update_traces(line_color="darkorange")
        fig.add_traces(prediction_fig.data)


def plot_ts(
        ts_data: pd.DataFrame,
        sub_region_codes: Optional[List[int]]=None
        ):
        """
        Plot time-series data
        """
        ts_data_to_plot = ts_data[ts_data.sub_region_code.isin(sub_region_codes)] if sub_region_codes else ts_data

        fig = px.line(ts_data_to_plot, x="date", y="demand", color="sub_region_code", template="none")

        fig.show()