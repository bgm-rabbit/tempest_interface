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

def test_main_temperature_graph(mock_input, mock_get_historical_obs, capsys):
    mock_input.side_effect = ['1', 'q']
    mock_get_historical_obs.return_value = pd.DataFrame({'temp_f': [50]})  # Minimal mock df
    with pytest.raises(SystemExit):
        main()
    captured = capsys.readouterr()
    assert "Fetched" in captured.out  # Check flow