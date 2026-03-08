# main.py
from api_client import get_historical_obs
from grapher import plot_temperature
import sys

def main():
    print("Tempest Weather Tool")
    print("1: Fetch & Graph Last 24h Temperature")
    print("2: Fetch & Save Last 24h Data (no graph)")
    print("q: Quit")

    choice = input("Enter choice: ").strip().lower()

    if choice == '1':
        try:
            df = get_historical_obs(hours_back=24)
            if df is not None:
                print(f"Fetched {len(df)} observations.")
                # Optional: print summary with local time
                print(df[['timestamp_local', 'temp_f', 'humidity_pct']].describe().round(1))
                plot_temperature(df)  # Assuming grapher.py uses 'timestamp' or update to 'timestamp_local'
            else:
                print("No data returned.")
        except Exception as e:
            print(f"Error fetching data: {e}")
    elif choice == '2':
        try:
            df = get_historical_obs(hours_back=24)
            df.to_csv('historical_24h.csv', index=False)
            print("Data saved to historical_24h.csv")
        except Exception as e:
            print(f"Error: {e}")
    elif choice in ['q', 'quit', 'exit']:
        sys.exit(0)
    else:
        print("Invalid choice.")

if __name__ == "__main__":
    main()