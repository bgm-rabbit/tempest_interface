# grapher.py
import matplotlib.pyplot as plt
import pandas as pd  # for cumsum/clip
import numpy as np  # For binning and averages

def plot_temperature(df, save_path='feels_like_24h.png', use_local_time=True, timeframe_str='Last 24 Hours'):
    time_col = 'timestamp_local' if use_local_time and 'timestamp_local' in df.columns else 'timestamp'
    
    plt.figure(figsize=(14, 7))
    
    # Air temperature
    plt.plot(df[time_col], df['temp_f'], color='orange', linewidth=2.5, marker='o', markersize=4, alpha=0.9, label='Air Temp (°F)')
    
    # Dew point
    valid_dew = df['dew_point_f'].notna()
    plt.plot(df[time_col][valid_dew], df['dew_point_f'][valid_dew], 
             color='purple', linewidth=2, linestyle='-', alpha=0.8, label='Dew Point (°F)')
    
    # Wind chill (only plot where it's lower than air temp)
    valid_chill = (df['wind_chill_f'] < df['temp_f']) & df['wind_chill_f'].notna()
    plt.plot(df[time_col][valid_chill], df['wind_chill_f'][valid_chill], 
             color='blue', linewidth=2, linestyle='--', label='Wind Chill (°F)')
    
    # Heat index (only plot where it's higher than air temp)
    valid_hi = (df['heat_index_f'] > df['temp_f']) & df['heat_index_f'].notna()
    plt.plot(df[time_col][valid_hi], df['heat_index_f'][valid_hi], 
             color='red', linewidth=2, linestyle='--', label='Heat Index (°F)')
    
    plt.title(f'Temperature, Dew Point, Wind Chill & Heat Index (Feels Like) – {timeframe_str} (°F)', fontsize=14)
    plt.xlabel('Time', fontsize=12)
    plt.ylabel('°F', fontsize=12)
    plt.legend(loc='best', fontsize=10)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(save_path)
    plt.show()
    print(f"Feels-like graph (Temp/Dew/Wind Chill/Heat Index) saved as {save_path}")

def plot_humidity(df, save_path='humidity_24h.png', use_local_time=True, timeframe_str='Last 24 Hours'):
    time_col = 'timestamp_local' if use_local_time and 'timestamp_local' in df.columns else 'timestamp'
    
    plt.figure(figsize=(12, 6))
    plt.plot(df[time_col], df['humidity_pct'], color='blue', linewidth=2, marker='o', markersize=3, alpha=0.8)
    plt.title(f'Relative Humidity Over {timeframe_str} (%)', fontsize=14)
    plt.xlabel('Time', fontsize=12)
    plt.ylabel('Humidity (%)', fontsize=12)
    plt.ylim(0, 100)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(save_path)
    plt.show()
    print(f"Humidity graph saved as {save_path}")

def plot_wind(df, save_path='wind_24h.png', use_local_time=True, timeframe_str='Last 24 Hours'):
    time_col = 'timestamp_local' if use_local_time and 'timestamp_local' in df.columns else 'timestamp'
    
    # Convert m/s to mph
    df['wind_avg_mph'] = (df['wind_avg_ms'] * 2.23694).round(1)
    df['wind_gust_mph'] = (df['wind_gust_ms'] * 2.23694).round(1)
    
    plt.figure(figsize=(12, 6))
    plt.plot(df[time_col], df['wind_avg_mph'], label='Average Wind', color='green', linewidth=2)
    plt.plot(df[time_col], df['wind_gust_mph'], label='Gust', color='red', linewidth=2, linestyle='--')
    plt.title(f'Wind Speed Over {timeframe_str} (mph)', fontsize=14)
    plt.xlabel('Time', fontsize=12)
    plt.ylabel('Wind Speed (mph)', fontsize=12)
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(save_path)
    plt.show()
    print(f"Wind graph saved as {save_path}")

def plot_pressure(df, save_path='pressure_24h.png', use_local_time=True, timeframe_str='Last 24 Hours'):
    time_col = 'timestamp_local' if use_local_time and 'timestamp_local' in df.columns else 'timestamp'
    
    # Convert mb to inHg
    df['pressure_inhg'] = (df['pressure_mb'] / 33.8639).round(2)
    
    plt.figure(figsize=(12, 6))
    plt.plot(df[time_col], df['pressure_inhg'], color='purple', linewidth=2, marker='o', markersize=3, alpha=0.8)
    plt.title(f'Barometric Pressure Over {timeframe_str} (inHg)', fontsize=14)
    plt.xlabel('Time', fontsize=12)
    plt.ylabel('Pressure (inHg)', fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(save_path)
    plt.show()
    print(f"Pressure graph saved as {save_path}")

def plot_solar_and_uv(df, save_path='solar_uv_24h.png', use_local_time=True, timeframe_str='Last 24 Hours'):
    time_col = 'timestamp_local' if use_local_time and 'timestamp_local' in df.columns else 'timestamp'
    
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
    
    plt.title(f'Solar Radiation & UV Index Over {timeframe_str}', fontsize=14)
    fig.legend(loc='upper right')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(save_path)
    plt.show()
    print(f"Solar & UV graph saved as {save_path}")

def plot_precip_accumulated(df, save_path='precip_24h.png', use_local_time=True, timeframe_str='Last 24 Hours'):
    time_col = 'timestamp_local' if use_local_time and 'timestamp_local' in df.columns else 'timestamp'
    
    # Cumulative precipitation, force non-negative
    df['precip_cumulative_mm'] = df['precip_mm_interval'].cumsum().clip(lower=0)
    df['precip_cumulative_in'] = (df['precip_cumulative_mm'] * 0.0393701).round(2)
    
    plt.figure(figsize=(12, 6))
    plt.plot(df[time_col], df['precip_cumulative_in'], color='cyan', linewidth=2.5)
    plt.title(f'Cumulative Precipitation Over {timeframe_str} (inches)', fontsize=14)
    plt.xlabel('Time', fontsize=12)
    plt.ylabel('Cumulative Rain (inches)', fontsize=12)
    plt.ylim(bottom=0)  # Explicitly start y-axis at 0
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(save_path)
    plt.show()
    print(f"Precipitation graph saved as {save_path}")

def plot_wind_rose(df, save_path='wind_rose_24h.png', timeframe_str='Last 24 Hours'):
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
    
    plt.title(f'Wind Rose: Direction Frequency & Avg Speed {timeframe_str}', fontsize=14)
    plt.tight_layout()
    plt.savefig(save_path)
    plt.show()
    print(f"Wind rose graph saved as {save_path}")