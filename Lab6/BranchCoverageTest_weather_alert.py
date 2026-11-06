import pytest
from weather_alert import wind_alert, rain_alert, heat_alert, overall_alert

"""
Test suite focused on Branch Coverage.
Ensures every decision branch (if/else, loops, boolean conditions) evaluates to both True and False,
including edge cases and boundary conditions.
Target: >90% to 100% branch coverage (Achieves 100% Branch Coverage).
"""

# ==========================================
# 1. Wind Alert Branch & Boundary Tests
# ==========================================
def test_wind_alert_warning_branch():
    # speed >= 89 (True branch)
    assert wind_alert(89) == "warning"
    assert wind_alert(120) == "warning"


def test_wind_alert_watch_branch():
    # speed >= 89 (False) and speed >= 62 (True)
    assert wind_alert(62) == "watch"
    assert wind_alert(88) == "watch"


def test_wind_alert_advisory_branch():
    # speed >= 89 (False), speed >= 62 (False), speed >= 39 (True)
    assert wind_alert(39) == "advisory"
    assert wind_alert(61) == "advisory"


def test_wind_alert_none_branch():
    # speed >= 89 (False), speed >= 62 (False), speed >= 39 (False)
    assert wind_alert(38) == "none"
    assert wind_alert(0) == "none"


# ==========================================
# 2. Rain Alert Branch & Boundary Tests
# ==========================================
def test_rain_alert_heavy_saturated_branch():
    # mm >= 50 (True), soil_saturated (True) -> "warning"
    assert rain_alert(50, True) == "warning"
    assert rain_alert(80, True) == "warning"


def test_rain_alert_heavy_dry_branch():
    # mm >= 50 (True), soil_saturated (False) -> "watch"
    assert rain_alert(50, False) == "watch"
    assert rain_alert(80, False) == "watch"


def test_rain_alert_moderate_saturated_branch():
    # mm >= 50 (False), mm >= 10 (True), soil_saturated (True) -> "watch"
    assert rain_alert(10, True) == "watch"
    assert rain_alert(49, True) == "watch"


def test_rain_alert_moderate_dry_branch():
    # mm >= 50 (False), mm >= 10 (True), soil_saturated (False) -> "advisory"
    assert rain_alert(10, False) == "advisory"
    assert rain_alert(49, False) == "advisory"


def test_rain_alert_light_rain_branch():
    # mm >= 50 (False), mm >= 10 (False) -> "none"
    # Testing both saturated and dry states for complete branch independence
    assert rain_alert(9, False) == "none"
    assert rain_alert(9, True) == "none"
    assert rain_alert(0, False) == "none"


# ==========================================
# 3. Heat Alert Branch & Boundary Tests
# ==========================================
def test_heat_alert_humidity_branch_above_40():
    # humidity > 40 (True branch: index adjusted)
    # temp = 40, humidity = 50 -> index = 40 + (10 * 0.1) = 41.0 -> "watch"
    assert heat_alert(40, 50) == "watch"


def test_heat_alert_humidity_branch_at_or_below_40():
    # humidity > 40 (False branch: index not adjusted)
    # boundary: humidity = 40
    assert heat_alert(40, 40) == "watch"
    # below boundary: humidity = 20
    assert heat_alert(40, 20) == "watch"


def test_heat_alert_warning_branch():
    # index >= 45 (True branch)
    # Exact boundary: temp=45, humidity=40 (no adjustment) -> 45
    assert heat_alert(45, 40) == "warning"
    # With humidity boost: temp=41, humidity=90 -> 41 + 5.0 = 46.0 -> "warning"
    assert heat_alert(41, 90) == "warning"


def test_heat_alert_watch_branch():
    # index >= 45 (False), index >= 40 (True)
    # Exact boundary: temp=40, humidity=40 -> 40
    assert heat_alert(40, 40) == "watch"
    # Just below warning: temp=44.9, humidity=40 -> 44.9
    assert heat_alert(44.9, 40) == "watch"


def test_heat_alert_advisory_branch():
    # index >= 40 (False), index >= 35 (True)
    # Exact boundary: temp=35, humidity=40 -> 35
    assert heat_alert(35, 40) == "advisory"
    # Just below watch: temp=39.9, humidity=40 -> 39.9
    assert heat_alert(39.9, 40) == "advisory"


def test_heat_alert_none_branch():
    # index >= 35 (False)
    # Just below advisory: temp=34.9, humidity=40 -> 34.9
    assert heat_alert(34.9, 40) == "none"
    assert heat_alert(25, 30) == "none"


# ==========================================
# 4. Overall Alert Branch & Loop Tests
# ==========================================
def test_overall_alert_empty_list():
    # Loop executes 0 times (for loop not entered branch)
    assert overall_alert([]) == "none"


def test_overall_alert_invalid_item():
    # if alert not in SEVERITY (True branch -> raise ValueError)
    with pytest.raises(ValueError, match="unknown alert"):
        overall_alert(["cyclone"])

    with pytest.raises(ValueError, match="unknown alert"):
        overall_alert(["advisory", "invalid_level", "warning"])


def test_overall_alert_escalating_severity():
    # if SEVERITY[alert] > SEVERITY[worst] (True branch -> worst updated)
    assert overall_alert(["none", "advisory", "watch", "warning"]) == "warning"


def test_overall_alert_non_escalating_severity():
    # if SEVERITY[alert] > SEVERITY[worst] (False branch -> worst retained, 44->41)
    # Case 1: subsequent alert has lower severity
    assert overall_alert(["warning", "advisory"]) == "warning"
    # Case 2: subsequent alert has identical severity
    assert overall_alert(["watch", "watch"]) == "watch"
    # Case 3: descending severity order
    assert overall_alert(["warning", "watch", "advisory", "none"]) == "warning"
