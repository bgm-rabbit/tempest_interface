# data_processor.py
import math
from datetime import datetime

import pandas as pd
import pytz

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

def process_observations(obs_list, local_tz_str='America/Chicago'):
    if not obs_list:
        return pd.DataFrame()  # Return empty df if no data

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
            'strike_count': obs[14],  # Strikes in interval (int)
            'strike_distance_km': obs[15],  # Distance to nearest (km, float)
        }
        records.append(record)

    df = pd.DataFrame(records)
    local_tz = pytz.timezone(local_tz_str)
    df['timestamp_local'] = df['timestamp'].dt.tz_localize('UTC').dt.tz_convert(local_tz)
    df = df.sort_values('timestamp_local').reset_index(drop=True)
    return df