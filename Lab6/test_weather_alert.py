import pytest
from weather_alert import wind_alert, rain_alert, heat_alert, overall_alert

# ============================================================================
# Lab 6: Code and Branch Coverage Analysis - Weather Alert Classifier
# Student Name: Prateek Hachadad
# SRN: PES1UG24CS340
# Section: F
# ============================================================================

# --- Wind Alert Tests ---
def test_calm_wind():
    assert wind_alert(10) == "none"
    assert wind_alert(38) == "none"

def test_wind_advisory():
    assert wind_alert(39) == "advisory"
    assert wind_alert(61) == "advisory"

def test_wind_watch():
    assert wind_alert(62) == "watch"
    assert wind_alert(88) == "watch"

def test_wind_warning():
    assert wind_alert(89) == "warning"
    assert wind_alert(120) == "warning"


# --- Rain Alert Tests ---
def test_rain_none():
    assert rain_alert(0, False) == "none"
    assert rain_alert(9, False) == "none"
    assert rain_alert(9, True) == "none"

def test_rain_advisory():
    assert rain_alert(10, False) == "advisory"
    assert rain_alert(49, False) == "advisory"

def test_rain_watch_moderate_saturated():
    assert rain_alert(10, True) == "watch"
    assert rain_alert(49, True) == "watch"

def test_rain_watch_heavy_dry():
    assert rain_alert(50, False) == "watch"
    assert rain_alert(75, False) == "watch"

def test_rain_warning_heavy_saturated():
    assert rain_alert(50, True) == "warning"
    assert rain_alert(80, True) == "warning"


# --- Heat Alert Tests ---
def test_heat_none():
    assert heat_alert(25, 30) == "none"
    assert heat_alert(34.9, 40) == "none"

def test_heat_advisory():
    assert heat_alert(35, 40) == "advisory"
    assert heat_alert(39.9, 40) == "advisory"

def test_heat_watch():
    assert heat_alert(40, 40) == "watch"
    assert heat_alert(44.9, 40) == "watch"
    # With humidity boost: 38 + (60 - 40) * 0.1 = 40.0
    assert heat_alert(38, 60) == "watch"

def test_heat_warning():
    assert heat_alert(45, 40) == "warning"
    # With humidity boost: 41 + (90 - 40) * 0.1 = 46.0
    assert heat_alert(41, 90) == "warning"


# --- Overall Alert Tests ---
def test_no_alerts():
    assert overall_alert([]) == "none"

def test_overall_alert_invalid_input():
    with pytest.raises(ValueError, match="unknown alert"):
        overall_alert(["storm"])

    with pytest.raises(ValueError, match="unknown alert"):
        overall_alert(["advisory", "blizzard"])

def test_overall_alert_escalating():
    assert overall_alert(["none", "advisory", "watch", "warning"]) == "warning"

def test_overall_alert_non_escalating():
    assert overall_alert(["warning", "advisory"]) == "warning"
    assert overall_alert(["watch", "watch"]) == "watch"
    assert overall_alert(["warning", "watch", "advisory", "none"]) == "warning"
