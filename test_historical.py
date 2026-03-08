# test_historical.py
import requests
import os
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
import pandas as pd
import matplotlib.pyplot as plt
import pytz


load_dotenv()
TOKEN = os.getenv('TOKEN')
DEVICE_ID = os.getenv('DEVICE_ID')

if not TOKEN or not DEVICE_ID:
    print("Missing TOKEN or DEVICE_ID in .env file!")
    exit(1)

def get_historical_obs(device_id, token, hours_back=24):
    now = datetime.now(timezone.utc)
    time_end = int(now.timestamp())
    time_start = int((now - timedelta(hours=hours_back)).timestamp())

    url = (f"https://swd.weatherflow.com/swd/rest/observations/device/{device_id}"
           f"?time_start={time_start}&time_end={time_end}&token={token}")
    
    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        data = response.json()

        obs_list = data.get('obs', [])
        if not obs_list:
            print("No historical observations returned. Check time range or device.")
            return None

        records = []
        for obs in obs_list:
            temp_c = obs[7]
            temp_f = round(temp_c * 9/5 + 32, 1)  # Convert and round to 1 decimal

            record = {
                'timestamp': datetime.fromtimestamp(obs[0]),
                'temp_f': temp_f,
                'temp_c': temp_c,                # Keep Celsius too if you want
                'humidity_pct': obs[8],
                'wind_avg_ms': obs[2],
                'wind_gust_ms': obs[3],
                'wind_dir_deg': obs[4],
                'pressure_mb': obs[6],
                'precip_mm_interval': obs[12],
                'uv_index': obs[10],
                'solar_rad_wm2': obs[11],
            }
            records.append(record)

        df = pd.DataFrame(records)
        local_tz = pytz.timezone('America/Chicago')
        df['timestamp_local'] = df['timestamp'].dt.tz_localize('UTC').dt.tz_convert(local_tz)
        df = df.sort_values('timestamp_local').reset_index(drop=True)
        return df

    except requests.RequestException as e:
        print(f"API request failed: {e}")
        if 'response' in locals() and hasattr(e.response, 'text'):
            print("Response details:", e.response.text)
        return None

# Fetch data
df_hist = get_historical_obs(DEVICE_ID, TOKEN, hours_back=24)

if df_hist is not None:
    print(f"\nHistorical Data (last 24 hours, {len(df_hist)} observations):")
    print(df_hist[['timestamp_local', 'temp_f', 'humidity_pct', 'wind_avg_ms', 
                   'precip_mm_interval']].head(8).to_string(index=False))
    print("\n... (showing first 8 and last few rows) ...")
    print(df_hist[['timestamp_local', 'temp_f', 'humidity_pct', 'wind_avg_ms', 
                   'precip_mm_interval']].tail(5).to_string(index=False))

    # Save full CSV
    csv_path = 'historical_24h.csv'
    df_hist.to_csv(csv_path, index=False)
    print(f"\nFull data saved to {csv_path}")

    # Summary stats (focus on key columns)
    print("\nQuick Summary (last 24h):")
    print(df_hist[['timestamp_local', 'temp_f', 'humidity_pct', 'wind_avg_ms', 'wind_gust_ms', 
               'precip_mm_interval']].head(8).to_string(index=False, float_format='%.1f'))

    # === Graph: Temperature over time ===
    plt.figure(figsize=(12, 6))
    plt.plot(df_hist['timestamp_local'], df_hist['temp_f'], 
             color='orange', linewidth=2, marker='o', markersize=3, alpha=0.8)
    plt.title('Temperature Over the Last 24 Hours (°F)', fontsize=14)
    plt.xlabel('Time (America/Chicago)', fontsize=12)
    plt.ylabel('Temperature (°F)', fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.xticks(rotation=45)
    plt.tight_layout()

    graph_path = 'temp_24h.png'
    plt.savefig(graph_path)
    plt.show()  # This will pop up the graph window on macOS
    print(f"Graph saved as {graph_path}")