# test_historical.py
import os
from dotenv import load_dotenv
import pandas as pd
import matplotlib.pyplot as plt
from api_client import get_historical_obs


load_dotenv()
TOKEN = os.getenv('TOKEN')
DEVICE_ID = os.getenv('DEVICE_ID')

if not TOKEN or not DEVICE_ID:
    print("Missing TOKEN or DEVICE_ID in .env file!")
    exit(1)

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