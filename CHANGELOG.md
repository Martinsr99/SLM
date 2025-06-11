# Changelog

All notable changes to AutoVolumeManager will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1] - 2025-06-11

### Added
- **Auto-detection of new audio applications**: UI automatically refreshes every 5 seconds to detect new audio sources
- **Mutual exclusion validation**: Apps can only be in Priority OR Music lists, not both
- **Comprehensive input validation**: All configuration values are validated and corrected automatically
- **Configuration cleaning**: Automatic removal of non-existent apps and duplicate entries
- **Real-time feedback**: Immediate application of volume changes when settings are modified
- **Enhanced error handling**: Robust validation in VolumeManager with proper fallbacks
- **Complete project restructure**: Organized code into modular packages (`src/config/`, `src/core/`, `src/ui/`)
- **Configuration template system**: Automatic generation of `config.template.json` with documentation
- **Enhanced UI**: Real-time value display on sliders with percentage and unit indicators
- **Build system**: Automated executable generation with PyInstaller

### Changed
- **Updated default values**: 
  - `volume_ducked`: 1.0 → 0.15 (15% volume when ducked)
  - `restore_delay`: 3.0 → 1.0 seconds (faster restoration)
- **Modern UI framework**: Upgraded to CustomTkinter for better appearance
- **Improved configuration management**: Centralized settings with validation
- **Enhanced logging**: More informative console messages for debugging and monitoring

### Fixed
- **Thread safety**: Fixed "dictionary changed size during iteration" error with proper thread-safe operations
- **Initialization order**: Resolved AttributeError by separating config validation phases
- **Dynamic app detection**: New audio applications now appear automatically without restart
- **Better error handling**: Graceful handling of configuration and runtime errors

### Technical Improvements
- **Modular architecture**: Complete code restructure with separated concerns
- **Type annotations**: Full type hints for better code maintainability
- **Input sanitization**: Validation of all user inputs and configuration data
- **Automatic cleanup**: Removal of invalid or non-existent applications from configuration
- **Package structure**: Proper Python package organization with `__init__.py` files
- **Import system**: Clean module imports and dependencies

## [1.0] - 2025-06-11

### Features
- Basic volume ducking functionality
- Simple UI interface
- Configuration file support
- Audio application detection
- Priority and music app selection
- Multi-language support (English and Spanish)
- Application hiding/showing functionality
- Customizable volume levels and thresholds

---

## Version Numbering

- **Major version** (X.0.0): Breaking changes or complete rewrites
- **Minor version** (X.Y.0): New features and significant improvements
- **Patch version** (X.Y.Z): Bug fixes and small improvements

## Categories

- **Added**: New features
- **Changed**: Changes in existing functionality
- **Deprecated**: Soon-to-be removed features
- **Removed**: Removed features
- **Fixed**: Bug fixes
- **Security**: Security improvements
- **Technical Improvements**: Code quality, performance, or architecture improvements
