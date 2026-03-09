# main.py
import sys
import os
from api_client import get_historical_obs
from grapher import (
    plot_temperature,
    plot_humidity,
    plot_wind,
    plot_pressure,
    plot_solar_and_uv,
    plot_precip_accumulated,
    plot_wind_rose,
    plot_lightning
)

current_start = None  # Global for custom start (str)
current_end = None    # Global for custom end (str)

def main():
    global current_start, current_end
    while True:
        print("\nTempest Weather Tool")
        print(f"Current Timeframe: {'Default 24h' if not current_start else f'{current_start} to {current_end} (local)'}")
        print("0: Set Custom Timeframe")
        print("1: Temperature and Dew Point Graph")
        print("2: Humidity Graph")
        print("3: Wind Speed Graph")
        print("4: Barometric Pressure Graph")
        print("5: Solar Radiation & UV Index Graph")
        print("6: Cumulative Precipitation Graph")
        print("7: Fetch & Save Data (CSV)")
        print("8: Wind Rose (Direction & Speed Summary)")
        print("9: Lightning Strikes Graph")
        print("q: Quit")

        choice = input("Enter choice: ").strip().lower()

        if choice == 'q' or choice == 'quit':
            print("Goodbye!")
            sys.exit(0)

        try:
            if choice == '0':  # Set timeframe
                print("Enter start time (YYYY-MM-DD HH:MM, local time; blank for 24h back):")
                new_start = input().strip() or None
                print("Enter end time (YYYY-MM-DD HH:MM, local time; blank for now):")
                new_end = input().strip() or None
                # Dry run to validate
                get_historical_obs(start_str=new_start, end_str=new_end)
                current_start = new_start
                current_end = new_end
                print("Timeframe updated.")
                continue

            df = get_historical_obs(start_str=current_start, end_str=current_end)
            if df is None:
                print("No data returned from API.")
                continue
            if df.empty:
                print("Fetched data is empty—check timeframe or station.")
                continue

            print(f"Fetched {len(df)} observations over selected timeframe.")

            use_local = 'timestamp_local' in df.columns
            timeframe_str = 'Last 24 Hours' if not current_start else f'{current_start} to {current_end}'

            if choice == '1':
                plot_temperature(df, use_local_time=use_local, timeframe_str=timeframe_str)
            elif choice == '2':
                plot_humidity(df, use_local_time=use_local, timeframe_str=timeframe_str)
            elif choice == '3':
                plot_wind(df, use_local_time=use_local, timeframe_str=timeframe_str)
            elif choice == '4':
                plot_pressure(df, use_local_time=use_local, timeframe_str=timeframe_str)
            elif choice == '5':
                plot_solar_and_uv(df, use_local_time=use_local, timeframe_str=timeframe_str)
            elif choice == '6':
                plot_precip_accumulated(df, use_local_time=use_local, timeframe_str=timeframe_str)
            elif choice == '7':
                # Dynamic name based on timeframe
                csv_name = f'historical_{current_start.replace(" ", "_") if current_start else "24h"}.csv'
                save_path = os.path.join('outputs', csv_name)
                df.to_csv(save_path, index=False)
                print(f"Data saved to {save_path}")
            elif choice == '8':
                plot_wind_rose(df, timeframe_str=timeframe_str)
            elif choice == '9':
                plot_lightning(df, use_local_time=use_local, timeframe_str=timeframe_str)
            else:
                print("Invalid choice. Try again.")

        except ValueError as ve:
            print(f"Input error: {ve}")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()