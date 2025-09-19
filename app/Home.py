"""Home Page of the Streamlit App"""

import streamlit as st
import os

from utils.data_loader import load_data


# App config
st.set_page_config(page_title="Spotify Analysis", page_icon="🎵", layout="wide")
st.title("🎵 Spotify Data Explorer")
st.write("Willkommen zur Streamlit App! Hier kannst du deine Spotify-Daten interaktiv erkunden.")

# Data Loading
DATA_PATH = os.path.join("data", "processed", "spotify_2023_cleaned.csv")

try:
    df = load_data(DATA_PATH)
    st.success(f"Daten geladen: {df.shape[0]} Zeilen, {df.shape[1]} Spalten")

    st.subheader("Datenvorschau")
    st.dataframe(df.head())

except FileNotFoundError:
    st.error(f"Datei nicht gefunden unter `{DATA_PATH}`.")
