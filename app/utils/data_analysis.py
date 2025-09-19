"""Functions for data analysis and processing."""

import pandas as pd


def get_top_tracks(df: pd.DataFrame):
    """Returns the top 10 tracks by popularity."""
    df_top_tracks = df.nlargest(10, 'streams')[['track_name', 'artist(s)_name', 'streams']]
    df_top_tracks['track_artist'] = df_top_tracks['track_name'] + ' - ' + df_top_tracks['artist(s)_name']

    return df_top_tracks[['track_artist', 'streams']].reset_index(drop=True)


def get_top_artists(df: pd.DataFrame):
    """Returns the top 10 tracks by popularity."""
    df_artists = df.copy()

    df_artists["artist_list"] = df_artists["artist(s)_name"].str.split(",")
    df_exploded = df_artists.explode("artist_list")
    df_exploded["artist"] = df_exploded["artist_list"].str.strip()
    df_exploded.drop(columns=["artist_list"], inplace=True)

    df_artists_grouped = (
        df_exploded.groupby("artist")
        .agg(total_streams=("streams", "sum"), track_count=("streams", "count"))
        .reset_index()
    )

    return df_artists_grouped.nlargest(10, 'total_streams')


def get_banger(df: pd.DataFrame):
    df_banger = df.copy()
    df_banger = df_banger[["track_name", "artist(s)_name", "streams", "released_year"]]
    df_banger_grouped = (
        df_banger.groupby("released_year")
        .agg(streams_max=("streams", "max"), streams_sum=("streams", "sum"))
        .sort_values(by="streams_sum", ascending=False)
    )
    return df_banger_grouped.reset_index()


def get_audio_features(df: pd.DataFrame):
    """Processes and returns audio features from the dataframe."""
    df_audio = df.copy()
    df_audio["mode"] = df_audio["mode"].map({"Major": 1, "Minor": 0})
    audio_features = ['streams', 'danceability_%', 'energy_%', 'valence_%', 'acousticness_%', 'instrumentalness_%', 'speechiness_%', 'liveness_%', 'mode']
    df_audio_features = df_audio[audio_features]

    return df_audio_features


def get_track_release_analysis(df: pd.DataFrame):
    """Analyzes track releases over the years."""
    df_release_time = df.copy()
    df_release_time = df_release_time.groupby("released_month") \
        .agg(total_streams=("streams", "sum"), count_tracks=('streams', 'count')) \
        .reset_index()

    return df_release_time


def get_track_releases(df: pd.DataFrame):
    """Analyzes track releases over the years."""
    df_release = df.copy()
    df_release = df_release.groupby("released_month") \
        .agg(total_streams=("streams", "sum"), count_tracks=('streams', 'count')) \
        .reset_index()

    return df_release
