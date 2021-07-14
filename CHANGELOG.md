# Changelog
All notable changes to this project will be documented in this file.

## [Unreleased]
### Add
- Server state elements and locks can be accessed not only via dict-like keys but also attribute names, #11.
### Fix
- An uninitialized key can be referred to via `server_state_lock` so that the lock can be used at the first initialization of that key, #10.

## [0.0.1] - 2021-07-11
### Added
- The first release including `server_state`, `server_state_lock`, and chat samples using them.
