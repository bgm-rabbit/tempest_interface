# tests/test_api_client.py
import pytest
from unittest.mock import patch, MagicMock
from datetime import datetime
from api_client import get_historical_obs  # Add other functions as needed
from data_processor import calculate_dew_point_c

def test_get_historical_obs_valid_range():
    with patch('requests.get') as mock_get:
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'obs': [[int(datetime.now().timestamp()), 0, 1, 2, 3, 4, 5, 6, 7, 50, 8, 9, 10, 0, 0, 0]]  # Sample obs
        }
        mock_get.return_value = mock_response
        
        df = get_historical_obs(hours_back=1)
        assert not df.empty
        assert 'temp_f' in df.columns
        assert 'timestamp_local' in df.columns  # Check timezone conversion

def test_get_historical_obs_invalid_range():
    with pytest.raises(ValueError):
        get_historical_obs(start_str='2026-03-10 00:00', end_str='2026-03-09 00:00')  # Start after end

def test_get_historical_obs_no_data():
    with patch('requests.get') as mock_get:
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'obs': []}  # Empty obs
        mock_get.return_value = mock_response
        
        df = get_historical_obs(hours_back=1)
        assert df is None or df.empty  # Depending on your function's return

def test_get_historical_obs_invalid_token(monkeypatch):
    monkeypatch.setattr('api_client.TOKEN', None)
    monkeypatch.setattr('api_client.DEVICE_ID', None)
    with pytest.raises(ValueError) as exc:
        get_historical_obs()
    assert "TOKEN or DEVICE_ID" in str(exc.value)

def test_calculate_dew_point():
    assert abs(calculate_dew_point_c(20, 50) - 9.3) < 0.1  # Tolerance for float approx

# Add similar for wind_chill, heat_index if not in test_calculations.py