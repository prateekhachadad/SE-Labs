# Lab 6: Code and Branch Coverage Analysis

**Course:** Software Engineering Laboratory  
**Topic:** Code Coverage and Branch Coverage Analysis  
**Student Name:** Prateek Hachadad  
**SRN:** PES1UG24CS340  
**Section:** F  
**Base Repository:** [L6_L7_32_weather_alert](https://github.com/SETAPESU26/L6_L7_32_weather_alert)  

---

## 1. Objectives

- Understand the practical differences between **Line Coverage** and **Branch Coverage**.
- Use Python's `coverage` tool and `pytest` framework to measure, analyze, and systematically improve test coverage.
- Interpret coverage reports (`coverage report -m`) and identify untested execution paths, edge cases, and decision branches.
- Develop targeted test suites achieving minimum 90% to 100% coverage.

---

## 2. Theoretical Background

| Coverage Type | Definition | Key Question Answered |
| :--- | :--- | :--- |
| **Line Coverage** | Measures the percentage of executable lines executed at least once during test execution. | *Did the execution flow pass through this line of code at least once?* |
| **Branch Coverage** | Measures the percentage of decision outcomes (e.g. `True` and `False` outcomes for `if`, `elif`, loops) evaluated during testing. | *Did every conditional branch evaluate to both True and False?* |
| **Path Coverage** | Measures all possible unique paths through a function from entry to exit. | *Were all combinatorial paths through the code traversed?* |
| **Function Coverage** | Measures the percentage of declared functions invoked during the tests. | *Was every function called at least once?* |

> **Key Insight:** Line coverage can provide a false sense of security. Even if 100% of lines are executed, critical alternate logical branches (such as when an `if` condition evaluates to `False`, or an unhandled edge condition occurs) may remain completely untested. Branch coverage forces testing of all logical outcomes.

---

## 3. Application Under Test: `weather_alert.py`

The module classifies meteorological sensor readings and computes alert levels based on severity (`none` < `advisory` < `watch` < `warning`):

1. **`wind_alert(speed_kmh)`**:
   - `speed_kmh >= 89`: `"warning"`
   - `speed_kmh >= 62`: `"watch"`
   - `speed_kmh >= 39`: `"advisory"`
   - `else`: `"none"`

2. **`rain_alert(mm_per_hour, soil_saturated)`**:
   - `mm_per_hour >= 50`: `"warning"` if `soil_saturated` else `"watch"`
   - `mm_per_hour >= 10`: `"watch"` if `soil_saturated` else `"advisory"`
   - `else`: `"none"`

3. **`heat_alert(temp_c, humidity)`**:
   - Computes adjusted heat index: `if humidity > 40: index += (humidity - 40) * 0.1`
   - `index >= 45`: `"warning"`
   - `index >= 40`: `"watch"`
   - `index >= 35`: `"advisory"`
   - `else`: `"none"`

4. **`overall_alert(alerts)`**:
   - Iterates through a list of alerts and finds the highest severity level.
   - Raises `ValueError("unknown alert")` if an unrecognized alert string is passed.

---

## 4. Test Suites and Execution Results

### 4.1 Initial Starter Coverage
- **Command:** `coverage run -m pytest test_weather_alert.py && coverage report -m`
- **Line Coverage:** 32% (missing 26 lines out of 38)
- **Branch Coverage:** 24% (missing 24 branches)

### 4.2 Step 5: Code Coverage Suite (`CodeCoverageTest_weather_alert.py`)
- **Focus:** Line coverage ensuring all statements across all 4 functions execute at least once.
- **Commands:**
  ```bash
  coverage run -m pytest CodeCoverageTest_weather_alert.py
  coverage report -m
  ```
- **Results:**
  ```
  Name                                Stmts   Miss  Cover   Missing
  -----------------------------------------------------------------
  CodeCoverageTest_weather_alert.py      36      0   100%
  weather_alert.py                       38      0   100%
  -----------------------------------------------------------------
  TOTAL                                  74      0   100%
  ```
- **Analysis:** Achieved **100% Line Coverage** (exceeding the >= 90% requirement). However, when evaluated for branch coverage (`--branch`), branch `44->41` in `overall_alert` was flagged as missing because the severity comparison `SEVERITY[alert] > SEVERITY[worst]` was never evaluated to `False` while inside the loop.

### 4.3 Step 7: Branch Coverage Suite (`BranchCoverageTest_weather_alert.py`)
- **Focus:** Complete decision branch coverage, boundary conditions, and edge cases.
- **Additions:**
  - Tested non-escalating and descending severity lists in `overall_alert` (exercises `44->41` False branch).
  - Tested humidity boundary conditions (`humidity <= 40` vs `humidity > 40`).
  - Tested exact threshold values for wind (`89`, `88`, `62`, `61`, `39`, `38`), rain (`50`, `49`, `10`, `9`), and heat (`45`, `44.9`, `40`, `39.9`, `35`, `34.9`).
  - Tested invalid alert validation in `overall_alert` with `pytest.raises(ValueError)`.
- **Commands:**
  ```bash
  coverage run --branch -m pytest BranchCoverageTest_weather_alert.py
  coverage report -m
  ```
- **Results:**
  ```
  Name                                  Stmts   Miss Branch BrPart  Cover   Missing
  ---------------------------------------------------------------------------------
  BranchCoverageTest_weather_alert.py      61      0      0      0   100%
  weather_alert.py                         38      0     28      0   100%
  ---------------------------------------------------------------------------------
  TOTAL                                    99      0     28      0   100%
  ```
- **Analysis:** Achieved **100% Branch Coverage** and **100% Line Coverage** (0 missing branches, 0 missing lines).

---

## 5. Deliverables Summary

| Deliverable | Description |
| :--- | :--- |
| `weather_alert.py` | Source application module under test |
| `test_weather_alert.py` | Consolidated pytest test suite |
| `CodeCoverageTest_weather_alert.py` | Test suite designed for code (line) coverage (>90%) |
| `BranchCoverageTest_weather_alert.py` | Test suite designed for branch coverage (>90% - 100%) |
| `code_coverage_analysis.png` | Terminal output screenshot for code coverage |
| `branch_coverage_analysis.png` | Terminal output screenshot for branch coverage |
| `PES1UG24CS340_Lab6.zip` | Archive containing all deliverables and git commit history |

---

## 6. How to Run

1. **Install requirements:**
   ```bash
   pip install coverage pytest
   ```

2. **Execute Code Coverage analysis:**
   ```bash
   coverage run -m pytest CodeCoverageTest_weather_alert.py
   coverage report -m
   ```

3. **Execute Branch Coverage analysis:**
   ```bash
   coverage run --branch -m pytest BranchCoverageTest_weather_alert.py
   coverage report -m
   ```
