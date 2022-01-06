# Changelog
All notable changes to this project will be documented in this file.

## [Unreleased]

## [0.10.0] - 2022-01-06
### Fix
- Internal type annotations to be compatible with streamlit>=1.3, #581.

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
