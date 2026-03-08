# test_latest.py
import requests
import os
from datetime import datetime
from dotenv import load_dotenv
import pandas as pd

load_dotenv()
TOKEN = os.getenv('TOKEN')
DEVICE_ID = os.getenv('DEVICE_ID')

if not TOKEN or not DEVICE_ID:
    print("Missing TOKEN or DEVICE_ID in .env file!")
    exit(1)

def get_latest_obs(device_id, token):
    url = f"https://swd.weatherflow.com/swd/rest/observations/device/{device_id}?token={token}"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()

        obs_list = data.get('obs', [])
        if not obs_list:
            print("No observations returned. Check device_id or token.")
            return None

        # Latest obs (most recent first)
        obs = obs_list[0]

        # Field order for Tempest (obs_st) - approximate/current common mapping:
        # 0:  time (unix seconds)
        # 1:  wind lull (m/s)
        # 2:  wind avg (m/s)
        # 3:  wind gust (m/s)
        # 4:  wind direction (degrees)
        # 5:  wind sample interval (s)
        # 6:  station pressure (mb)
        # 7:  air temperature (C)
        # 8:  relative humidity (%)
        # 9:  illuminance (lux)
        # 10: UV index
        # 11: solar radiation (W/m²)
        # 12: precip accumulated (mm, local over reporting interval)
        # 13: precip type (0=none, 1=rain, 2=hail)
        # 14: lightning strike count (in interval)
        # ... (more like battery, etc.)

        record = {
        'timestamp': datetime.fromtimestamp(obs[0]),
        'temp_f': round(obs[7] * 9/5 + 32, 1),         # Convert here directly
        'humidity_pct': obs[8],
        'wind_avg_ms': obs[2],
        'wind_gust_ms': obs[3],
        'wind_dir_deg': obs[4],
        'pressure_mb': obs[6],
        'precip_mm_interval': obs[12],
        'uv_index': round(obs[10], 1),
        'solar_rad_wm2': obs[11],
}

        df = pd.DataFrame([record])
        return df

    except requests.RequestException as e:
        print(f"API request failed: {e}")
        if 'response' in locals() and hasattr(e.response, 'text'):
            print("Response details:", e.response.text)
        return None

df = get_latest_obs(DEVICE_ID, TOKEN)
if df is not None:
    print("\nLatest Observation from Your Tempest Station (Device 205042):")
    print(df.to_string(index=False))
    df.to_csv('latest_obs.csv', index=False)
    print("\nSaved to latest_obs.csv")