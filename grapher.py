# grapher.py
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd  # for cumsum/clip
import numpy as np  # For binning and averages


OUT_DIR = Path('outputs')


def _ensure_output_dir():
    OUT_DIR.mkdir(exist_ok=True)


def _finalize_plot(save_path: str, show: bool, message: str):
    """Save the current matplotlib figure and optionally show it."""
    _ensure_output_dir()
    final_path = OUT_DIR / save_path
    plt.savefig(final_path)
    if show:
        plt.show()
    print(message.format(save_path=final_path))


def _style_axes(ax, title: str, xlabel: str, ylabel: str, rotate_xticks: int = 45, show_grid: bool = True):
    """Apply consistent styling to a matplotlib Axes."""
    ax.set_title(title, fontsize=14)
    ax.set_xlabel(xlabel, fontsize=12)
    ax.set_ylabel(ylabel, fontsize=12)
    if show_grid:
        ax.grid(True, linestyle='--', alpha=0.7)
    for label in ax.get_xticklabels():
        label.set_rotation(rotate_xticks)


def _prepare_plot(df, required_cols=None, use_local_time=True, graph_name='graph'):
    """Validate input dataframe and figure out which time column to use.

    Returns the time column name if valid, otherwise None.
    """
    if df is None or df.empty:
        print(f"No data available for {graph_name}.")
        return None

    time_col = 'timestamp_local' if use_local_time and 'timestamp_local' in df.columns else 'timestamp'
    if time_col not in df.columns:
        print(f"Required time column missing for {graph_name}.")
        return None

    if required_cols:
        missing = [c for c in required_cols if c not in df.columns]
        if missing:
            print(f"Required columns missing for {graph_name}: {missing}")
            return None

    return time_col


def plot_temperature(df, save_path='feels_like_24h.png', use_local_time=True, timeframe_str='Last 24 Hours', show=True):
    time_col = _prepare_plot(df, required_cols=['temp_f'], use_local_time=use_local_time, graph_name='temperature graph')
    if not time_col:
        return

    plt.figure(figsize=(14, 7))
    
    # Air temperature
    plt.plot(df[time_col], df['temp_f'], color='orange', linewidth=2.5, marker='o', markersize=4, alpha=0.9, label='Air Temp (°F)')
    
    # Dew point (optional)
    if 'dew_point_f' in df.columns:
        valid_dew = df['dew_point_f'].notna()
        plt.plot(df[time_col][valid_dew], df['dew_point_f'][valid_dew], 
                 color='purple', linewidth=2, linestyle='-', alpha=0.8, label='Dew Point (°F)')
    
    # Wind chill (only plot where it's lower than air temp)
    if 'wind_chill_f' in df.columns:
        valid_chill = (df['wind_chill_f'] < df['temp_f']) & df['wind_chill_f'].notna()
        plt.plot(df[time_col][valid_chill], df['wind_chill_f'][valid_chill], 
                 color='blue', linewidth=2, linestyle='--', label='Wind Chill (°F)')
    
    # Heat index (only plot where it's higher than air temp)
    if 'heat_index_f' in df.columns:
        valid_hi = (df['heat_index_f'] > df['temp_f']) & df['heat_index_f'].notna()
        plt.plot(df[time_col][valid_hi], df['heat_index_f'][valid_hi], 
                 color='red', linewidth=2, linestyle='--', label='Heat Index (°F)')
    
    ax = plt.gca()
    _style_axes(ax, f'Temperature, Dew Point, Wind Chill & Heat Index (Feels Like) – {timeframe_str} (°F)', 'Time', '°F')
    ax.legend(loc='best', fontsize=10)
    plt.tight_layout()
    _finalize_plot(save_path, show, "Feels-like graph (Temp/Dew/Wind Chill/Heat Index) saved as {save_path}")

def plot_humidity(df, save_path='humidity_24h.png', use_local_time=True, timeframe_str='Last 24 Hours', show=True):
    time_col = _prepare_plot(df, required_cols=['humidity_pct'], use_local_time=use_local_time, graph_name='humidity graph')
    if not time_col:
        return

    plt.figure(figsize=(12, 6))
    plt.plot(df[time_col], df['humidity_pct'], color='blue', linewidth=2, marker='o', markersize=3, alpha=0.8)
    ax = plt.gca()
    _style_axes(ax, f'Relative Humidity Over {timeframe_str} (%)', 'Time', 'Humidity (%)')
    ax.set_ylim(0, 100)
    plt.tight_layout()
    _finalize_plot(save_path, show, "Humidity graph saved as {save_path}")

def plot_wind(df, save_path='wind_24h.png', use_local_time=True, timeframe_str='Last 24 Hours', show=True):
    time_col = _prepare_plot(df, required_cols=['wind_avg_ms'], use_local_time=use_local_time, graph_name='wind graph')
    if not time_col:
        return

    # Convert m/s to mph if possible
    df['wind_avg_mph'] = (df['wind_avg_ms'] * 2.23694).round(1)

    if 'wind_gust_ms' in df.columns:
        df['wind_gust_mph'] = (df['wind_gust_ms'] * 2.23694).round(1)
    else:
        df['wind_gust_mph'] = np.nan

    plt.figure(figsize=(12, 6))
    plt.plot(df[time_col], df['wind_avg_mph'], label='Average Wind', color='green', linewidth=2)
    if 'wind_gust_ms' in df.columns:
        plt.plot(df[time_col], df['wind_gust_mph'], label='Gust', color='red', linewidth=2, linestyle='--')
    ax = plt.gca()
    _style_axes(ax, f'Wind Speed Over {timeframe_str} (mph)', 'Time', 'Wind Speed (mph)')
    ax.legend()
    plt.tight_layout()
    _finalize_plot(save_path, show, "Wind graph saved as {save_path}")

def plot_pressure(df, save_path='pressure_24h.png', use_local_time=True, timeframe_str='Last 24 Hours', show=True):
    time_col = _prepare_plot(df, required_cols=['pressure_mb'], use_local_time=use_local_time, graph_name='pressure graph')
    if not time_col:
        return
    
    # Convert mb to inHg
    df['pressure_inhg'] = (df['pressure_mb'] / 33.8639).round(2)
    
    plt.figure(figsize=(12, 6))
    plt.plot(df[time_col], df['pressure_inhg'], color='purple', linewidth=2, marker='o', markersize=3, alpha=0.8)
    ax = plt.gca()
    _style_axes(ax, f'Barometric Pressure Over {timeframe_str} (inHg)', 'Time', 'Pressure (inHg)')
    plt.tight_layout()
    _finalize_plot(save_path, show, "Pressure graph saved as {save_path}")

def plot_solar_and_uv(df, save_path='solar_uv_24h.png', use_local_time=True, timeframe_str='Last 24 Hours', show=True):
    time_col = _prepare_plot(df, required_cols=['solar_rad_wm2', 'uv_index'], use_local_time=use_local_time, graph_name='solar & UV graph')
    if not time_col:
        return
    
    fig, ax1 = plt.subplots(figsize=(12, 6))
    
    ax1.plot(df[time_col], df['solar_rad_wm2'], color='gold', linewidth=2, label='Solar Radiation (W/m²)')
    ax1.set_xlabel('Time', fontsize=12)
    ax1.set_ylabel('Solar Radiation (W/m²)', color='gold', fontsize=12)
    ax1.tick_params(axis='y', labelcolor='gold')
    ax1.grid(True, linestyle='--', alpha=0.7)
    
    ax2 = ax1.twinx()
    ax2.plot(df[time_col], df['uv_index'], color='violet', linewidth=2, label='UV Index')
    ax2.set_ylabel('UV Index', color='violet', fontsize=12)
    ax2.tick_params(axis='y', labelcolor='violet')
    
    _style_axes(ax1, f'Solar Radiation & UV Index Over {timeframe_str}', 'Time', 'Solar Radiation (W/m²)')
    _style_axes(ax2, '', '', 'UV Index', show_grid=False)
    fig.legend(loc='upper right')
    plt.tight_layout()
    _finalize_plot(save_path, show, "Solar & UV graph saved as {save_path}")

def plot_precip_accumulated(df, save_path='precip_24h.png', use_local_time=True, timeframe_str='Last 24 Hours', show=True):
    time_col = _prepare_plot(df, required_cols=['precip_mm_interval'], use_local_time=use_local_time, graph_name='precipitation graph')
    if not time_col:
        return
    
    # Cumulative precipitation, force non-negative
    df['precip_cumulative_mm'] = df['precip_mm_interval'].cumsum().clip(lower=0)
    df['precip_cumulative_in'] = (df['precip_cumulative_mm'] * 0.0393701).round(2)
    
    plt.figure(figsize=(12, 6))
    plt.plot(df[time_col], df['precip_cumulative_in'], color='cyan', linewidth=2.5)
    ax = plt.gca()
    _style_axes(ax, f'Cumulative Precipitation Over {timeframe_str} (inches)', 'Time', 'Cumulative Rain (inches)')
    ax.set_ylim(bottom=0)  # Explicitly start y-axis at 0
    plt.tight_layout()
    _finalize_plot(save_path, show, "Precipitation graph saved as {save_path}")

def plot_wind_rose(df, save_path='wind_rose_24h.png', timeframe_str='Last 24 Hours', show=True):
    required_cols = ['wind_dir_deg', 'wind_avg_mph']
    if df is None or df.empty:
        print("No data available for wind rose plot.")
        return

    missing = [c for c in required_cols if c not in df.columns]
    if missing:
        print(f"Required columns missing for wind rose plot: {missing}")
        return

    # Filter valid data
    valid = df['wind_dir_deg'].notna() & df['wind_avg_mph'].notna()
    directions = df['wind_dir_deg'][valid]
    speeds = df['wind_avg_mph'][valid]
    
    if len(directions) == 0:
        print("No valid wind data for rose plot.")
        return

    # 16 bins for compass directions
    num_bins = 16
    bin_edges = np.linspace(0, 360, num_bins + 1)
    bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2
    
    # Histogram: frequency per bin
    freq, _ = np.histogram(directions, bins=bin_edges)
    freq = freq / len(directions) * 100  # % frequency
    
    # Average speed per bin
    avg_speeds = []
    for i in range(num_bins):
        in_bin = (directions >= bin_edges[i]) & (directions < bin_edges[i+1])
        avg_speeds.append(speeds[in_bin].mean() if in_bin.any() else 0)
    
    # Plot polar bar chart
    fig = plt.figure(figsize=(8, 8))
    ax = fig.add_subplot(111, polar=True)
    
    # Bars: height=freq, width=2π/num_bins, color by avg speed
    width = 2 * np.pi / num_bins
    colors = plt.cm.viridis(np.array(avg_speeds) / max(avg_speeds + [1]))  # Normalize colors
    bars = ax.bar(np.deg2rad(bin_centers), freq, width=width, bottom=0.0, color=colors, edgecolor='grey')
    
    # Compass labels
    ax.set_theta_zero_location('N')
    ax.set_theta_direction(-1)  # Clockwise like compass
    ax.set_xticks(np.linspace(0, 2*np.pi, 8, endpoint=False))
    ax.set_xticklabels(['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW'])
    
    # Colorbar for avg speed
    sm = plt.cm.ScalarMappable(cmap=plt.cm.viridis, norm=plt.Normalize(0, max(avg_speeds)))
    cbar = plt.colorbar(sm, ax=ax, pad=0.1)
    cbar.set_label('Avg Wind Speed (mph)')
    
    ax.set_title(f'Wind Rose: Direction Frequency & Avg Speed {timeframe_str}', fontsize=14)
    plt.tight_layout()
    _finalize_plot(save_path, show, "Wind rose graph saved as {save_path}")

def plot_lightning(df, save_path='lightning_24h.png', use_local_time=True, timeframe_str='Last 24 Hours', show=True):
    if df is None or df.empty:
        print("No lightning strikes detected in timeframe—graph will be empty.")
        return

    time_col = _prepare_plot(df, required_cols=['strike_count', 'strike_distance_km'], use_local_time=use_local_time, graph_name='lightning graph')
    if not time_col:
        return

    # Aggregate hourly: sum strikes, average distance (only where strikes >0)
    df.set_index(time_col, inplace=True)
    hourly_strikes = df['strike_count'].resample('h').sum().fillna(0)
    hourly_distance_km = df[df['strike_count'] > 0]['strike_distance_km'].resample('h').mean().fillna(0)  # 0 if no strikes
    
    # Convert km to miles
    hourly_distance_mi = (hourly_distance_km * 0.621371).round(1)
    
    if hourly_strikes.sum() == 0:
        print("No lightning strikes detected in timeframe—graph will be empty.")
    
    fig, ax1 = plt.subplots(figsize=(12, 6))
    
    # Bar: Strikes per hour (left y)
    ax1.bar(hourly_strikes.index, hourly_strikes, width=0.03, color='red', alpha=0.7, label='Strikes per Hour')
    ax1.set_xlabel('Time', fontsize=12)
    ax1.set_ylabel('Strike Count per Hour', color='red', fontsize=12)
    ax1.tick_params(axis='y', labelcolor='red')
    ax1.grid(True, linestyle='--', alpha=0.7)
    
    # Line: Avg distance in miles (right y, only show if strikes)
    ax2 = ax1.twinx()
    ax2.plot(hourly_distance_mi.index, hourly_distance_mi, color='blue', linewidth=2.5, marker='o', label='Avg Strike Distance (miles)')
    ax2.set_ylabel('Average Distance (miles)', color='blue', fontsize=12)
    ax2.tick_params(axis='y', labelcolor='blue')
    
    ax1.set_title(f'Lightning Strikes: Count per Hour & Average Distance (miles) – {timeframe_str}', fontsize=14)
    fig.legend(loc='upper right', fontsize=10)
    for label in ax1.get_xticklabels():
        label.set_rotation(45)
    plt.tight_layout()
    _finalize_plot(save_path, show, "Lightning graph saved as {save_path}")
    
    # Reset index if needed
    df.reset_index(inplace=True)