# tests/test_grapher.py
import pytest
import pandas as pd
from grapher import (
    plot_temperature, plot_humidity, plot_wind, plot_pressure, 
    plot_solar_and_uv, plot_precip_accumulated, plot_wind_rose, plot_lightning
)  # Import all relevant plots

@pytest.fixture
def sample_df():
    return pd.DataFrame({
        'timestamp_local': pd.date_range(start='2026-03-08', periods=5, freq='h'),
        'temp_f': [50, 52, 55, 53, 51],
        'dew_point_f': [40, 42, 45, 43, 41],
        'wind_chill_f': [48, 50, 53, 51, 49],
        'heat_index_f': [52, 54, 57, 55, 53],
        'humidity_pct': [60, 65, 70, 68, 62],
        'wind_avg_ms': [2, 3, 2.5, 3.5, 2],
        'wind_gust_ms': [4, 5, 4.5, 5.5, 4],
        'wind_dir_deg': [180, 200, 190, 210, 185],
        'pressure_mb': [1010, 1012, 1011, 1013, 1010],
        'uv_index': [2, 3, 4, 3.5, 2.5],
        'solar_rad_wm2': [300, 400, 500, 450, 350],
        'precip_mm_interval': [0, 0.5, 0, 1, 0],
        'strike_count': [0, 1, 0, 2, 0],
        'strike_distance_km': [0, 10, 0, 5, 0]
    })

@pytest.fixture
def empty_df():
    return pd.DataFrame()  # For no-data tests

def test_plot_temperature(sample_df):
    try:
        plot_temperature(sample_df, show=False)
    except Exception as e:
        pytest.fail(f"Failed: {e}")

def test_plot_humidity(sample_df):
    try:
        plot_humidity(sample_df, show=False)
    except Exception as e:
        pytest.fail(f"Failed: {e}")

def test_plot_wind(sample_df):
    try:
        plot_wind(sample_df, show=False)
    except Exception as e:
        pytest.fail(f"Failed: {e}")

def test_plot_pressure(sample_df):
    try:
        plot_pressure(sample_df, show=False)
    except Exception as e:
        pytest.fail(f"Failed: {e}")

def test_plot_solar_and_uv(sample_df):
    try:
        plot_solar_and_uv(sample_df, show=False)
    except Exception as e:
        pytest.fail(f"Failed: {e}")

def test_plot_precip_accumulated(sample_df):
    try:
        plot_precip_accumulated(sample_df, show=False)
    except Exception as e:
        pytest.fail(f"Failed: {e}")

def test_plot_wind_rose(sample_df):
    try:
        plot_wind_rose(sample_df, show=False)
    except Exception as e:
        pytest.fail(f"Failed: {e}")

def test_plot_lightning(sample_df):
    try:
        plot_lightning(sample_df, show=False)
    except Exception as e:
        pytest.fail(f"Failed: {e}")

def test_plot_temperature_empty(empty_df):
    try:
        plot_temperature(empty_df, show=False)
    except Exception as e:
        pytest.fail(f"Failed on empty data: {e}")

def test_plot_lightning_empty(empty_df, capsys):
    try:
        plot_lightning(empty_df, show=False)
    except Exception as e:
        pytest.fail(f"Failed on empty data: {e}")
    captured = capsys.readouterr()
    assert "No lightning strikes detected" in captured.out  # Check warning message