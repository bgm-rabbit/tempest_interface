# api_client.py
import requests
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
import os
import pandas as pd
import pytz

load_dotenv()
TOKEN = os.getenv('TOKEN')
DEVICE_ID = os.getenv('DEVICE_ID')

def get_historical_obs(hours_back=24):
    if not TOKEN or not DEVICE_ID:
        raise ValueError("Missing TOKEN or DEVICE_ID in .env file")

    now = datetime.now(timezone.utc)
    time_end = int(now.timestamp())
    time_start = int((now - timedelta(hours=hours_back)).timestamp())

    url = (f"https://swd.weatherflow.com/swd/rest/observations/device/{DEVICE_ID}"
           f"?time_start={time_start}&time_end={time_end}&token={TOKEN}")
    
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
            temp_f = round(temp_c * 9/5 + 32, 1)

            record = {
                'timestamp': datetime.fromtimestamp(obs[0]),
                'temp_f': temp_f,
                'temp_c': temp_c,
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