# tests/test_calculations.py
from data_processor import calculate_wind_chill_f, calculate_heat_index_f, calculate_dew_point_c

def test_wind_chill():
    assert calculate_wind_chill_f(40, 10) < 40  # Wind chill lowers perceived temp
    assert calculate_wind_chill_f(60, 2) == 60  # No effect above thresholds
    assert calculate_wind_chill_f(30, 0) == 30  # No wind
    assert calculate_wind_chill_f(50, 20) == 50  # Temp at threshold

def test_heat_index():
    assert calculate_heat_index_f(90, 70) > 90  # Increases with humidity
    assert calculate_heat_index_f(70, 50) == 70  # No effect below thresholds
    assert calculate_heat_index_f(85, 90) > 85  # High RH adjustment
    assert calculate_heat_index_f(100, 10) < 100  # Low RH adjustment (if your function handles it)

def test_dew_point():
    assert abs(calculate_dew_point_c(20, 50) - 9.3) < 0.1  # Normal case
    assert calculate_dew_point_c(20, 0) is None  # Invalid low RH
    assert calculate_dew_point_c(20, 101) is None  # Invalid high RH
    assert abs(calculate_dew_point_c(0, 100) - 0) < 0.1  # At freezing with saturation
    assert abs(calculate_dew_point_c(30, 80) - 26.2) < 0.1  # Humid hot day