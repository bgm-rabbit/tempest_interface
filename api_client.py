# api_client.py
import requests
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
import os
import pytz
from data_processor import process_observations  # New import

load_dotenv()
TOKEN = os.getenv('TOKEN')
DEVICE_ID = os.getenv('DEVICE_ID')

def get_historical_obs(hours_back=24, start_str=None, end_str=None, local_tz_str='America/Chicago'):
    if not TOKEN or not DEVICE_ID:
        raise ValueError("Missing TOKEN or DEVICE_ID in .env file")

    local_tz = pytz.timezone(local_tz_str)
    now_local = datetime.now(local_tz)
    now_utc = now_local.astimezone(pytz.utc)

    # Default: last 24h if no inputs
    if not start_str:
        start_utc = now_utc - timedelta(hours=24)
    else:
        try:
            start_local = local_tz.localize(datetime.strptime(start_str, '%Y-%m-%d %H:%M'))
            start_utc = start_local.astimezone(pytz.utc)
        except ValueError:
            raise ValueError("Invalid start format. Use 'YYYY-MM-DD HH:MM' (24h).")

    if not end_str:
        end_utc = now_utc
    else:
        try:
            end_local = local_tz.localize(datetime.strptime(end_str, '%Y-%m-%d %H:%M'))
            end_utc = end_local.astimezone(pytz.utc)
        except ValueError:
            raise ValueError("Invalid end format. Use 'YYYY-MM-DD HH:MM' (24h).")

    # Check duration (warn if >5 days)
    duration_days = (end_utc - start_utc).days
    if duration_days > 5:
        print("Warning: API may return aggregated/low-res data for >5 days. Consider using /stats for summaries.")

    time_start = int(start_utc.timestamp())
    time_end = int(end_utc.timestamp())

    if time_start >= time_end:
        raise ValueError("Start time must be before end time.")

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

        # Process the raw obs_list
        df = process_observations(obs_list, local_tz_str=local_tz_str)
        return df

    except requests.RequestException as e:
        print(f"API request failed: {e}")
        if 'response' in locals() and hasattr(e.response, 'text'):
            print("Response details:", e.response.text)
        return None