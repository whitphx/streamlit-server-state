# Changelog
All notable changes to this project will be documented in this file.

## [Unreleased]

## [0.18.2] - 2024-10-24
### Fix
- Packaging pipeline update.

## [0.18.1]
Skipped

## [0.18.0] - 2024-10-24
### Change
- Support Streamlit>=1.38.0, #233.
- Drop Python 3.8 support, #233.

## [0.17.1] - 2023-08-21
### Fix
- Fix `get_session_info` to use `SessionManager.get_session_info()` instead of `.get_active_session_info()` because the session info sometimes can be inactive when accessed from this library, #202.

## [0.17.0] - 2023-08-20
### CHANGE
- Drop Python 3.7 support, #199.

## [0.16.1] - 2023-06-17
### Fix
- Support Python 3.11, #188.

## [0.16.0] - 2023-03-08
### Fix
- Introduce customized error classes, #176.

## [0.15.2] - 2023-02-16
### Fix
- Compatibility with streamlit>=1.18.0, #172, #175.
- Refactoring the sample chat apps, #174.

## [0.15.0] - 2022-11-24
### Add
- The `no_rerun` context manager to suppress re-running the app upon value assignment, #155.

## [0.14.2] - 2022-09-04
### Fix
- Catch `ReferenceError` during searching the server object , #139.

## [0.14.1] - 2022-08-27
### Fix
- Compatibility with streamlit>=1.12.1, #136.

## [0.14.0] - 2022-08-15
### Fix
- Use `packaging` for version comparison, #132.

## [0.13.0] - 2022-08-15
### Fix
- Escape-hatch to access the running Streamlit server object for the new web server design with streamlit>=1.12.0, #131.

## [0.12.2] - 2022-04-04
### Fix
- Rename internal imports to be compatible with streamlit>=1.8.0, #94.

## [0.12.1] - 2022-01-19
### Fix
- Fix `del server_state[key]` to work correctly, #71.

## [0.12.0] - 2022-01-15
### Fix
- Rename internal imports to be compatible with streamlit>=1.4.0, #63.

## [0.11.0] - 2022-01-06
### Fix
- Drop Python 3.6 support, #58.

## [0.10.0] - 2022-01-06
### Fix
- Internal type annotations to be compatible with streamlit>=1.3, #54.

## [0.9.0] - 2021-10-04
### Fix
- `obj.__dict__` is also considered when hashing, #42.

## [0.8.0] - 2021-10-04
### Add
- Add `force_rerun_bound_sessions()`, #40.

## [0.7.0] - 2021-09-30
### Fix
- Fix rerunning sessions inside callbacks to work correctly, #38.

## [0.6.1] - 2021-09-10
### Fix
- Fix `server_state_lock`, #34.

## [0.6.0] - 2021-09-09
### Fix
- Use `repr()` to compare objects to detect mutable objects diffs, #30.
- Fix an internal item key name, #33.

## [0.5.0] - 2021-09-06
### Fix
- Fix to rerun the sessions when the set values have been changed, #28.

## [0.4.0] - 2021-08-24
### Fix
- Set `client_state=None` option on `session.request_rerun()` to be compatible with streamlit>=0.87.0, #21.

## [0.3.0] - 2021-08-08
### Add
- multiprocessing compatibility, #18.

## [0.2.0] - 2021-07-14
### Add
- Server state elements and locks can be accessed not only via dict-like keys but also attribute names, #11.
### Fix
- An uninitialized key can be referred to via `server_state_lock` so that the lock can be used at the first initialization of that key, #10.

## [0.1.0] - 2021-07-11
### Added
- The first release including `server_state`, `server_state_lock`, and chat samples using them.
