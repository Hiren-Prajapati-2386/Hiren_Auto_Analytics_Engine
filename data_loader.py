import pandas as pd
import streamlit as st

@st.cache_data
def load_and_clean_data(filepath):
    df = pd.read_csv(filepath)
    df['month'] = pd.to_datetime(df['month'])
    return df