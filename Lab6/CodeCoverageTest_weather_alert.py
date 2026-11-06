import pytest
from weather_alert import wind_alert, rain_alert, heat_alert, overall_alert

"""
Test suite focused on Code Coverage (Line Coverage).
Ensures that every line of code across all functions in weather_alert.py executes at least once.
Target: >90% code (line) coverage (Achieves 100% line coverage).
"""

# --- Wind Alert Tests ---
def test_calm_wind():
    # Covers line 11 (returns "none")
    assert wind_alert(10) == "none"


def test_wind_advisory():
    # Covers lines 9, 10 (returns "advisory")
    assert wind_alert(45) == "advisory"


def test_wind_watch():
    # Covers lines 7, 8 (returns "watch")
    assert wind_alert(65) == "watch"


def test_wind_warning():
    # Covers lines 5, 6 (returns "warning")
    assert wind_alert(95) == "warning"


# --- Rain Alert Tests ---
def test_rain_none():
    # Covers line 23 (returns "none")
    assert rain_alert(5, False) == "none"


def test_rain_advisory():
    # Covers lines 19, 22 (returns "advisory")
    assert rain_alert(20, False) == "advisory"


def test_rain_watch_moderate():
    # Covers lines 19, 20, 21 (returns "watch")
    assert rain_alert(20, True) == "watch"


def test_rain_watch_heavy():
    # Covers lines 15, 18 (returns "watch")
    assert rain_alert(60, False) == "watch"


def test_rain_warning():
    # Covers lines 15, 16, 17 (returns "warning")
    assert rain_alert(60, True) == "warning"


# --- Heat Alert Tests ---
def test_heat_none():
    # Covers line 36 (returns "none")
    assert heat_alert(30, 30) == "none"


def test_heat_advisory():
    # Covers lines 34, 35 (returns "advisory")
    assert heat_alert(36, 30) == "advisory"


def test_heat_watch():
    # Covers lines 32, 33 (returns "watch")
    assert heat_alert(41, 30) == "watch"


def test_heat_warning_with_humidity():
    # Covers lines 28, 29, 30, 31 (humidity > 40 and returns "warning")
    # index = 42 + (50 - 40) * 0.1 = 43.0; with temp 45, index = 45 + 1.0 = 46.0 >= 45
    assert heat_alert(44, 60) == "warning"


# --- Overall Alert Tests ---
def test_no_alerts():
    # Covers lines 40, 46 (empty alerts returns "none")
    assert overall_alert([]) == "none"


def test_overall_alert_escalation():
    # Covers lines 41, 42, 44, 45, 46 (loops through, checks severity, updates worst)
    assert overall_alert(["advisory", "warning"]) == "warning"


def test_overall_alert_invalid_input():
    # Covers lines 41, 42, 43 (raises ValueError for unknown alert)
    with pytest.raises(ValueError, match="unknown alert"):
        overall_alert(["hurricane"])
