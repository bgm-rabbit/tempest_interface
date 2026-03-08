# api_client.py
import requests
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
import os
import pandas as pd
import pytz
import math

load_dotenv()
TOKEN = os.getenv('TOKEN')
DEVICE_ID = os.getenv('DEVICE_ID')

def calculate_wind_chill_f(temp_f, wind_mph):
    if wind_mph < 3 or temp_f >= 50:
        return round(temp_f, 1)
    v_pow = wind_mph ** 0.16
    wc = 35.74 + 0.6215 * temp_f - 35.75 * v_pow + 0.4275 * temp_f * v_pow
    return round(wc, 1)

def calculate_heat_index_f(temp_f, rh):
    if temp_f < 80:
        return round(temp_f, 1)  # HI not typically applied below 80°F
    # Rothfusz regression (NOAA official)
    hi = (
        -42.379 +
        2.04901523 * temp_f +
        10.14333127 * rh -
        0.22475541 * temp_f * rh -
        0.00683783 * temp_f**2 -
        0.05481717 * rh**2 +
        0.00122874 * temp_f**2 * rh +
        0.00085282 * temp_f * rh**2 -
        0.00000199 * temp_f**2 * rh**2
    )
    # Simple adjustments for edge cases (per NWS)
    if rh < 13 and 80 <= temp_f <= 112:
        adjustment = ((13 - rh) / 4) * math.sqrt((17 - math.fabs(temp_f - 95)) / 17)
        hi -= adjustment
    elif rh > 85 and 80 <= temp_f <= 87:
        adjustment = ((rh - 85) / 10) * ((87 - temp_f) / 5)
        hi += adjustment
    return round(hi, 1)

def calculate_dew_point_c(temp_c, humidity_pct):
    if humidity_pct <= 0 or humidity_pct > 100:
        return None  # Invalid RH
    a = 17.27
    b = 237.7  # °C
    alpha = math.log(humidity_pct / 100.0) + (a * temp_c) / (b + temp_c)
    dew_c = (b * alpha) / (a - alpha)
    return round(dew_c, 1)

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

        records = []
        for obs in obs_list:
            temp_c = obs[7]
            humidity = obs[8]
            wind_avg_ms = obs[2]
            temp_f = round(temp_c * 9/5 + 32, 1)
            dew_c = calculate_dew_point_c(temp_c, humidity)
            dew_f = round(dew_c * 9/5 + 32, 1) if dew_c is not None else None
            # Wind in mph (use avg for chill/HI; gust could be separate if desired)
            wind_avg_mph = wind_avg_ms * 2.23694
        
            wind_chill_f = calculate_wind_chill_f(temp_f, wind_avg_mph)
            heat_index_f = calculate_heat_index_f(temp_f, humidity)

            record = {
                'timestamp': datetime.fromtimestamp(obs[0]),
                'temp_f': temp_f,
                'temp_c': temp_c,
                'humidity_pct': obs[8],
                'dew_point_f': dew_f,
                'dew_point_c': dew_c,
                'wind_avg_mph': round(wind_avg_mph, 1),  # Add for convenience
                'wind_chill_f': wind_chill_f,
                'heat_index_f': heat_index_f,
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