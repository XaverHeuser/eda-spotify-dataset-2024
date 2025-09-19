import streamlit as st
import pandas as pd

@st.cache_data
def load_data(path):
    """Loads data from a CSV file and caches the result."""
    return pd.read_csv(path)