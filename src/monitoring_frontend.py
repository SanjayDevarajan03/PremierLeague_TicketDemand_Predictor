from datetime import datetime,timedelta, timezone
import numpy as np
import pandas as pd
import streamlit as st
from sklearn.metrics import mean_absolute_error
import plotly.express as px

from src.components.monitoring import load_predictions_and_actual_values_from_store

st.set_page_config(layout="wide")

# title
current_date = pd.to_datetime(datetime.now(tz=timezone.utc), utc=True).floor('H')
st.title(f"Monitoring dashboard")

progress_bar = st.sidebar.header('Working progress')
progress_bar = st.sidebar.progress(0)
N_STEPS = 3


with st.spinner(text="Fetching model predictions and actual values from the store"):
    monitoring_df = load_predictions_and_actual_values_from_store(
        from_date=current_date-timedelta(days=14),
        to_date=current_date
    )
    st.sidebar.write('Model predictions and actual values arrived')
    progress_bar.progress(1/N_STEPS)
    print(monitoring_df)
    print("Unique hours in dataset:", monitoring_df['actual_date'].dt.hour.unique())

with st.spinner(text="Plotting aggregate MAE hour-by-hour"):
    st.header('Mean Absolute Error (MAE) hour-by-hour')

    # MAE per pickup_hour
    mae_per_hour = (
        monitoring_df.groupby('actual_date').apply(lambda g: mean_absolute_error(g['actual_demand'], g['predicted_demand']))
        .reset_index()
        .rename(columns={0:'mae'})
        .sort_values(by='actual_date')
    )

    fig = px.bar(mae_per_hour,x='actual_date', y='mae', template='plotly_dark')
    st.plotly_chart(fig, theme="streamlit", use_container_width=True, width=1000)

    progress_bar.progress(2/N_STEPS)

with st.spinner(text="Plotting MAE hour-by-hour for top locations"):
    st.header('Mean Absolute Error (MAE) per location and hour')

    top_locations_by_demand=(monitoring_df.groupby('actual_sub_region_code')['actual_demand'].sum()
                            .sort_values(ascending=False)
                            .reset_index()
                            .head(6)['actual_sub_region_code'])
    

    for location_id in top_locations_by_demand:
        mae_per_hour = (
            monitoring_df[monitoring_df.actuals_sub_region_code==location_id]
            .groupby('actual_date')
            .apply(lambda g: mean_absolute_error(g['actual_demand'], g['predicted_demand']))
            .reset_index()
            .rename(columns={0:'mae'})
            .head(6)['actual_sub_region_code']
        )

        fig = px.bar(mae_per_hour,
                     x='actual_date', y='mae',
                     template='plotly_dark')
        
        st.subheader(f'{location_id=}')
        st.plotly_chart(fig, theme="streamlit", use_container_width=True, width=1000)

    progress_bar.progress(3/N_STEPS)