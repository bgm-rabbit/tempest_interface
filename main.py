# main.py
from api_client import get_historical_obs
from grapher import (
    plot_temperature,
    plot_humidity,
    plot_wind,
    plot_pressure,
    plot_solar_and_uv,
    plot_precip_accumulated,
    plot_wind_rose
)
import sys

current_start = None  # Global for custom start (str)
current_end = None    # Global for custom end (str)

def main():
    global current_start, current_end
    while True:
        print("\nTempest Weather Tool")
        print(f"Current Timeframe: {'Default 24h' if not current_start else f'{current_start} to {current_end} (local)'}")
        print("0: Set Custom Timeframe")
        print("1: Temperature and Dew Point Graph (24h)")
        print("2: Humidity Graph (24h)")
        print("3: Wind Speed Graph (24h)")
        print("4: Barometric Pressure Graph (24h)")
        print("5: Solar Radiation & UV Index Graph (24h)")
        print("6: Cumulative Precipitation Graph (24h)")
        print("7: Fetch & Save 24h Data (CSV)")
        print("8: Wind Rose (Direction & Speed Summary, 24h)")
        print("q: Quit")

        choice = input("Enter choice: ").strip().lower()

        if choice == 'q' or choice == 'quit':
            print("Goodbye!")
            sys.exit(0)

        try:
            if choice == '0':  # New: Set timeframe
                print("Enter start time (YYYY-MM-DD HH:MM, local time; blank for 24h back):")
                new_start = input().strip() or None
                print("Enter end time (YYYY-MM-DD HH:MM, local time; blank for now):")
                new_end = input().strip() or None
                # Test parse to validate
                get_historical_obs(start_str=new_start, end_str=new_end)  # Dry run to check
                current_start = new_start
                current_end = new_end
                print("Timeframe updated.")
                continue

            df = get_historical_obs(start_str=current_start, end_str=current_end)
            if df is None:
                print("No data returned from API.")
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
                save_path = 'historical_data.csv'  # Or dynamic name with dates
                df.to_csv(save_path, index=False)
                print(f"Data saved to {save_path}")
            elif choice == '8':
                plot_wind_rose(df)
            else:
                print("Invalid choice. Try again.")

        except ValueError as ve:
            print(f"Input error: {ve}")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()