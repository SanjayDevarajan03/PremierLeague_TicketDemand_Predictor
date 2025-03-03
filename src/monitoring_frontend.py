from datetime import datetime,timedelta, timezone
import numpy as np
import pandas as pd
import streamlit as st
from sklearn.metrics import mean_absolute_error
import plotly.express as px

from src.components.monitoring import load_predictions_and_actual_values_from_store

st.set_page_config(layout="wide")