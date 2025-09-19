"""Home Page of the Streamlit App"""
import numpy as np
import streamlit as st
import seaborn as sns
import pandas as pd
import os

from matplotlib import pyplot as plt

from utils.data_analysis import (
    get_top_artists,
    get_top_tracks,
    get_audio_features,
    get_banger,
    get_track_releases,
)
from utils.data_loader import load_data


# App config
st.set_page_config(page_title='Spotify Analysis', page_icon='🎵', layout='wide')
st.title('🎵 Spotify Data Explorer')
st.write('Welcome to the Spotify Data Explorer! Use the tabs to navigate through different sections of the app.')

# Data Loading
DATA_PATH = os.path.join('data', 'processed', 'spotify_2023_cleaned.csv')

try:
    df = load_data(DATA_PATH)
    st.success(f'Daten geladen: {df.shape[0]} Zeilen, {df.shape[1]} Spalten')

except FileNotFoundError:
    df = pd.DataFrame()
    st.error(f'Datei nicht gefunden unter `{DATA_PATH}`.')


#################
# Tabs
#################
tabs = st.tabs(['Preview', 'Top Tracks and Artists', 'Audio Features', 'Release Analysis'])

with tabs[0]:
    st.header('Preview')
    st.info('A preview of the loaded dataset is shown below.')
    st.dataframe(df.head())

with tabs[1]:
    st.header('Top Tracks and Artists')

    #################
    # Top Tracks
    #################
    df_top_tracks = get_top_tracks(df)

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(
        x="streams", y="track_artist", data=df_top_tracks, palette="viridis", ax=ax
    )
    ax.set_xlabel("Streams")
    ax.set_ylabel("Track Name")
    ax.set_title("Top 10 Most Streamed Tracks in 2023")
    st.pyplot(fig)

    ##################
    # Top Artists
    ##################
    df_top_artists = get_top_artists(df)

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(
        x="total_streams", y="artist", data=df_top_artists, palette="magma", ax=ax
    )
    ax.set_xlabel("Streams")
    ax.set_ylabel("Artist Name")
    ax.set_title("Top 10 Most Streamed Artists in 2023")
    st.pyplot(fig)


    ##################
    # Bangers
    ##################
    df_bangers = get_banger(df)
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(
        x="released_year", y="streams_max", data=df_bangers, palette="plasma", ax=ax
    )
    ax.set_xlabel("Release Year")
    ax.set_ylabel("Streams")
    ax.set_title("Streams of the Most Streamed Track by Release Year")
    st.pyplot(fig)

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(
        x="released_year", y="streams_sum", data=df_bangers, palette="plasma", ax=ax
    )
    ax.set_xlabel("Release Year")
    ax.set_ylabel("Total Streams")
    ax.set_title("Total Streams by Release Year")
    st.pyplot(fig)


with tabs[2]:
    st.header('Audio Features')

    df_audio_features = get_audio_features(df)
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.heatmap(
        df_audio_features.corr(),
        annot=True,
        cmap="coolwarm",
        fmt=".2f",
        linewidths=0.5,
        ax=ax,
    )
    ax.set_title("Correlation Heatmap of Audio Features and Streams")
    fig.tight_layout()
    st.pyplot(fig)


with tabs[3]:
    st.header('Track Release Analysis')

    df_track_release = get_track_releases(df)

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(
        x="released_month", y="total_streams", data=df_track_release, ax=ax
    )
    ax.set_xlabel("Release Month")
    ax.set_ylabel("Total Streams")
    ax.set_title("Total Streams by Release Month in 2023")
    fig.tight_layout()
    st.pyplot(fig)

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(
        x="released_month", y="count_tracks", data=df_track_release, palette="coolwarm", ax=ax
    )
    ax.set_xlabel("Release Month")
    ax.set_ylabel("Number of Tracks Released")
    ax.set_title("Number of Tracks Released by Month in 2023")
    fig.tight_layout()
    st.pyplot(fig)
