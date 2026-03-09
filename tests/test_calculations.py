# tests/test_calculations.py
from api_client import calculate_wind_chill_f, calculate_heat_index_f, calculate_dew_point_c

def test_wind_chill():
    assert calculate_wind_chill_f(40, 10) < 40
    assert calculate_wind_chill_f(60, 2) == 60

def test_heat_index():
    assert calculate_heat_index_f(90, 70) > 90
    assert calculate_heat_index_f(70, 50) == 70

def test_dew_point():
    assert abs(calculate_dew_point_c(20, 50) - 9.3) < 0.1
    assert calculate_dew_point_c(20, 0) is None  # Invalid RH