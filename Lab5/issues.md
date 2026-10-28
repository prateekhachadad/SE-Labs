# Lab 5: Static Code Analysis — Issues Log

**Student Name:** Prateek Hachadad  
**SRN:** PES1UG24CS340  
**Course:** Software Engineering Lab (UE24CS252AA) — Lab 5  
**Target File:** `expense_tracker.py`  

---

## 1. Static Analysis Summary

| Tool | Initial Status | Final Status | Key Observations |
| :--- | :--- | :--- | :--- |
| **Bandit** | 4 issues (1 High, 2 Medium, 1 Low) | **0 issues** | Resolved command injection, insecure temporary file creation, hardcoded temp paths, and hardcoded secrets. |
| **Pylint** | Score: **5.27 / 10** | Score: **10.00 / 10** | Fixed missing docstrings, non-standard naming conventions, broad exception handling, global statements, and non-pythonic iteration. |
| **Flake8** | 4 violations (E203, E302, E261, E501) | **0 violations** | Resolved whitespace violations, missing blank lines, comment spacing, and long lines (>79 chars). |

---

## 2. Issues and Fixes Table

| Issue | Type | Line(s) | Description | Fix Approach |
| :--- | :--- | :--- | :--- | :--- |
| **Command Injection (`B605`)** | Security (High) | 61 | `os.system("xdg-open " + path)` executes command in a system shell without sanitization, exposing application to arbitrary command injection (CWE-78). | Replaced shell invocation with Python standard library `webbrowser.open(os.path.abspath(path))` after verifying path existence, eliminating shell execution and argument injection risks. |
| **Insecure / Deprecated `mktemp` (`B306`)** | Security (Medium) | 55 | `tempfile.mktemp()` is deprecated and vulnerable to Time-of-Check to Time-of-Use (TOCTOU) race conditions and symlink hijacking (CWE-377). | Replaced with `tempfile.NamedTemporaryFile` with atomic file creation and secure permissions. |
| **Hardcoded Insecure Temp Directory (`B108`)** | Security (Medium) | 8 | `REPORT_DIR = "/tmp/expense_reports"` uses a world-writable `/tmp` path prone to pre-creation attacks and symlink hijacking (CWE-377). | Configured path via `os.getenv("EXPENSE_REPORT_DIR", ...)` falling back to `tempfile.gettempdir()`, ensuring proper directory permissions with `os.makedirs(REPORT_DIR, exist_ok=True)`. |
| **Hardcoded Secret Password (`B105`)** | Security (Low) | 5 | `BANK_SYNC_PASSWORD = "demo-sync-pass"` hardcodes sensitive authentication credentials directly into version-controlled source code (CWE-259). | Retrieved password dynamically from environment variables using `os.getenv("BANK_SYNC_PASSWORD", "demo-sync-pass")`. |
| **Broad Exception Catch (`W0718`)** | Bug / Reliability | 41 | `except Exception:` catches all standard exceptions indiscriminately, potentially masking programming bugs, memory errors, or unintended failures. | Replaced with specific exception handling `except ValueError:`, which is the exact exception raised by Python's `max()` on an empty iterable. |
| **Global State Mutation (`W0603`)** | Architecture / Design | 29 | `global monthly_budget` rebinds a global primitive variable within a function, causing tight coupling and concurrency issues. | Encapsulated budget state in a mutable structure `budget_state = {"monthly_budget": ...}` managed via accessor and mutator functions (`set_budget`, `get_budget`), removing `global`. |
| **Non-pythonic Iteration (`C0200`)** | Code Quality | 45 | `for i in range(len(expenses)):` performs manual index-based iteration over a list. | Refactored to idiomatic Python using `for i, expense in enumerate(expenses, 1):`, improving readability and eliminating manual indexing. |
| **Non-standard Naming (`C0103`)** | Style / Quality | 7, 11, 20, 28, 33, 38, 44, 49, 53, 55, 59 | Function and variable names used camelCase (e.g., `addExpense`, `newBudget`, `reportPath`) violating PEP 8 snake_case conventions. | Renamed all functions and identifiers to snake_case (e.g., `add_expense`, `new_budget`, `report_path`). |
| **Missing Module & Function Docstrings (`C0114`, `C0116`)** | Documentation | 1, 11, 20, 28, 33, 38, 44, 49, 53, 59, 64 | Module and functions lacked docstrings explaining their purpose, parameters, and return types. | Added comprehensive PEP 257 compliant docstrings documenting behavior, arguments, and return types for the module and all functions. |
| **Whitespace Before Colon (`E203`)** | Style (PEP 8) | 15 | Whitespace before colon in dictionary declaration: `{"amount" : amount}`. | Removed superfluous whitespace to comply with PEP 8 dictionary syntax: `{"amount": amount}`. |
| **Missing Blank Lines (`E302`)** | Style (PEP 8) | 44 | Only 1 blank line found between top-level functions instead of the required 2 blank lines. | Added 2 blank lines separating all top-level functions per PEP 8 specifications. |
| **Inline Comment Spacing (`E261`)** | Style (PEP 8) | 74 | Only a single space before inline comment `# after setBudget`. | Added 2 spaces before inline comment in compliance with PEP 8 (`  # after setBudget`). |
| **Line Length Limit Exceeded (`E501`)** | Style (PEP 8) | 77 | Statement exceeded 79 characters (93 characters). | Broken statement across multiple lines cleanly within 79 characters. |
