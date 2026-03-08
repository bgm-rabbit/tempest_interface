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

def main():
    while True:
        print("\nTempest Weather Tool")
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
            df = get_historical_obs(hours_back=24)
            if df is None:
                print("No data returned from API.")
                continue

            print(f"Fetched {len(df)} observations.")

            use_local = 'timestamp_local' in df.columns

            if choice == '1':
                plot_temperature(df, use_local_time=use_local)
            elif choice == '2':
                plot_humidity(df, use_local_time=use_local)
            elif choice == '3':
                plot_wind(df, use_local_time=use_local)
            elif choice == '4':
                plot_pressure(df, use_local_time=use_local)
            elif choice == '5':
                plot_solar_and_uv(df, use_local_time=use_local)
            elif choice == '6':
                plot_precip_accumulated(df, use_local_time=use_local)
            elif choice == '7':
                df.to_csv('historical_24h.csv', index=False)
                print("Data saved to historical_24h.csv")
            elif choice == '8':
                plot_wind_rose(df)
            else:
                print("Invalid choice. Try again.")

        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()