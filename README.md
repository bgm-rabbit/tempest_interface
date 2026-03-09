# Tempest Weather Tool

A Python command-line tool to interface with your Tempest Weather station API, fetch historical data, process it with derived metrics (e.g., dew point, wind chill, heat index), and generate visualizations like graphs and charts. Built as a personal project for analyzing local weather in Kansas City, MO (or any Tempest station location).

## Features
- Fetch current and historical weather data from your Tempest device.
- Process raw data with unit conversions (°C to °F, m/s to mph, mb to inHg, km to miles, mm to inches).
- Derived calculations: Dew point, wind chill, heat index.
- Interactive CLI menu for:
  - Custom timeframes (e.g., specific date ranges).
  - Graphs: Temperature (with feels-like), humidity, wind speed, pressure, solar/UV, precipitation, wind rose, lightning strikes.
  - CSV data export.
- Robust error handling and input validation.
- Unit tests with pytest for reliability.

## Prerequisites
- Python 3.10+ (tested on 3.14).
- Tempest Weather station with a personal access token (PAT) from app.tempestwx.com/settings/data-authorizations.
- macOS, Linux, or Windows (developed on macOS 12 with Homebrew).

## Installation
1. Clone or download the project:
    git clone https://github.com/bgm-rabbit/tempest_interface.git
    cd tempest_interface

2. Create and activate a virtual environment:
    python -m venv venv
    source venv/bin/activate  # On macOS/Linux

3. Install dependencies:
    pip install -r requirements.txt

4. Configure .env:
- Copy .env.example to .env.
- Add your TOKEN and DEVICE_ID (from Tempest app).

## Usage
Run the app:
    python3 main.py

- Follow the menu prompts:
  - 0: Set custom timeframe (local time, e.g., "2026-03-08 00:00" to "2026-03-09 12:00").
  - 1-9: Generate graphs (saved to outputs/ folder as PNGs).
  - 7: Export data to CSV in outputs/.
  - q: Quit.

Example output files:
- outputs/feels_like_24h.png (temperature graph)
- outputs/historical_data.csv

## Testing
Run unit/integration tests:
    pytest -v
- Covers API fetching, calculations, graphs, and CLI flows.
- Use `pytest --cov=.` for coverage report (requires pytest-cov).

## Folder Structure
- `main.py`: CLI entry point.
- `api_client.py`: API fetching and raw data retrieval.
- `data_processor.py`: Data transformations and calculations.
- `grapher.py`: Visualization functions.
- `tests/`: Pytest files for unit/integration testing.
- `outputs/`: Generated graphs and CSVs (git-ignored).

## Notes
- API limits: Tempest allows ~1000 calls/day; use responsibly.
- Timezone: Defaults to 'America/Chicago' (Kansas City)—customize in code if needed.
- Developed in March 2026—update dependencies as Python evolves.
- Future ideas: GUI with Streamlit, forecasts via OpenWeatherMap, alerts.

## License
MIT License (or your choice)—feel free to use/modify.

