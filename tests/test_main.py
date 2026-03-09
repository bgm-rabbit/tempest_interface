# tests/test_main.py
import pytest
import pandas as pd
from io import StringIO
from unittest.mock import patch
import sys
from main import main  # Import your main function

@pytest.fixture
def mock_input():
    with patch('builtins.input') as patched:
        yield patched

@pytest.fixture
def mock_get_historical_obs():
    with patch('main.get_historical_obs') as patched:
        yield patched

@pytest.fixture
def mock_plot_temperature():
    with patch('main.plot_temperature') as patched:
        yield patched

# Add mocks for other plots as needed, e.g., mock_plot_humidity = patch('main.plot_humidity')

def test_main_quit(mock_input, capsys):
    mock_input.side_effect = ['q']
    with pytest.raises(SystemExit):
        main()
    captured = capsys.readouterr()
    assert "Goodbye!" in captured.out

def test_main_invalid_choice(mock_input, capsys):
    mock_input.side_effect = ['invalid', 'q']
    with pytest.raises(SystemExit):
        main()
    captured = capsys.readouterr()
    assert "Invalid choice" in captured.out

@pytest.mark.parametrize("choice, expected_output_snippet", [
    ('1', "Fetched"),  # Temperature graph
    # You can add more choices once the corresponding plot functions are mocked
    # ('2', "Fetched"),  # Humidity
    # ('3', "Fetched"),  # Wind
])
def test_main_graph_choices(mock_input, mock_get_historical_obs, mock_plot_temperature, capsys, choice, expected_output_snippet):
    mock_input.side_effect = [choice, 'q']  # Choose graph then quit
    mock_get_historical_obs.return_value = pd.DataFrame({'temp_f': [50]})  # Minimal df
    with pytest.raises(SystemExit):
        main()
    captured = capsys.readouterr()
    assert expected_output_snippet in captured.out
    if choice == '1':
        mock_plot_temperature.assert_called_once()  # Verify plot was called (for choice 1)

def test_main_csv_save(mock_input, mock_get_historical_obs, capsys):
    mock_input.side_effect = ['7', 'q']
    mock_get_historical_obs.return_value = pd.DataFrame({'temp_f': [50]})
    with pytest.raises(SystemExit):
        main()
    captured = capsys.readouterr()
    assert "Data saved to" in captured.out

def test_main_fetch_error(mock_input, mock_get_historical_obs, capsys):
    mock_input.side_effect = ['1', 'q']
    mock_get_historical_obs.side_effect = ValueError("API error")
    with pytest.raises(SystemExit):
        main()
    captured = capsys.readouterr()
    assert "Input error" in captured.out
    assert "API error" in captured.out

# Add if you have timeframe setting
def test_main_set_timeframe(mock_input, capsys):
    mock_input.side_effect = ['0', '2026-03-08 00:00', '', 'q']  # Start date, blank end (now)
    with pytest.raises(SystemExit):
        main()
    captured = capsys.readouterr()
    assert "Timeframe updated" in captured.out