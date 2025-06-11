# AutoVolumeManager

Automatic volume ducking application that lowers music volume when priority audio applications are detected.

## Features

- **Automatic Volume Ducking**: Automatically reduces music volume when priority applications (like Discord, Teams, etc.) have audio activity
- **Real-time Configuration**: All settings apply immediately without restart
- **Multi-language Support**: English and Spanish interface
- **Application Management**: Hide/show applications from the interface
- **Customizable Settings**: Adjustable volume levels, thresholds, and delays
- **Modern UI**: Clean, responsive interface with dark/light themes

## Project Structure

```
AutoVolumeManager_v1/
├── src/                          # Source code
│   ├── config/                   # Configuration management
│   │   ├── __init__.py
│   │   ├── settings.py           # Configuration loading/saving
│   │   └── languages.py          # Language definitions
│   ├── core/                     # Core functionality
│   │   ├── __init__.py
│   │   ├── audio_utils.py        # Audio system utilities
│   │   └── volume_manager.py     # Volume management logic
│   ├── ui/                       # User interface
│   │   ├── __init__.py
│   │   └── main_window.py        # Main application window
│   └── __init__.py
├── main.py                       # Application entry point
├── config.template.json          # Configuration template
├── requirements.txt              # Python dependencies
├── .gitignore                    # Git ignore rules
└── README.md                     # This file
```

## Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd AutoVolumeManager_v1
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**:
   ```bash
   python main.py
   ```

## Building Executable

To create a standalone .exe file:

1. **Install PyInstaller**:
   ```bash
   python -m pip install --user pyinstaller
   ```

2. **Build the executable**:
   ```bash
   python -m PyInstaller --onefile --windowed --name AutoVolumeManager --add-data "config.template.json;." --hidden-import customtkinter --hidden-import pycaw --hidden-import comtypes main.py
   ```

3. **Find your executable**:
   - The .exe file will be created in the `dist/` folder
   - Copy `AutoVolumeManager.exe` from `dist/` folder to distribute
   - The executable includes all dependencies and can run on any Windows system

**Build Parameters Explained**:
- `--onefile`: Creates a single executable file
- `--windowed`: Hides the console window (GUI only)
- `--name`: Sets the executable name
- `--add-data`: Includes the config template file
- `--hidden-import`: Ensures required modules are included

## Configuration

The application creates a `config.template.json` file on first run that shows all available configuration options. Your personal settings are saved in `config.json` (which is ignored by git).

### Configuration Options

- **volume_normal**: Normal volume level (0.0 to 1.0)
- **volume_ducked**: Reduced volume level when priority audio is detected (0.0 to 1.0)
- **peak_threshold**: Audio peak threshold to trigger ducking (0.0 to 1.0)
- **restore_delay**: Delay in seconds before restoring normal volume
- **priority_apps**: List of applications that trigger volume ducking
- **music_apps**: List of music applications to be ducked
- **ignored_apps**: List of applications to hide from the interface
- **appearance_mode**: UI appearance mode ('dark' or 'light')
- **language**: Interface language ('en' or 'es')

## Usage

1. **Setup Priority Apps**: Select applications that should trigger volume ducking (e.g., Discord, Teams, Zoom)
2. **Setup Music Apps**: Select music applications that should be ducked (e.g., Spotify, iTunes, YouTube Music)
3. **Adjust Settings**: Use the sliders to configure volume levels, sensitivity, and timing
4. **Real-time Updates**: All changes apply immediately while the application is running

## Requirements

- Windows 10/11
- Python 3.7+
- Audio applications with Windows audio sessions

## Dependencies

- `customtkinter`: Modern UI framework
- `pycaw`: Windows Core Audio API wrapper
- `comtypes`: COM interface support

## Development

### Code Organization

- **src/config/**: Configuration management and language support
- **src/core/**: Core audio processing and volume management
- **src/ui/**: User interface components
- **main.py**: Application entry point and initialization

### Key Features

- **Thread-safe**: UI and audio monitoring run in separate threads
- **Modular Design**: Clean separation of concerns
- **Type Hints**: Full type annotation support
- **Error Handling**: Robust error handling and logging
- **Immediate Updates**: Configuration changes apply instantly

## Troubleshooting

### Common Issues

1. **No audio applications detected**: Make sure applications are playing audio
2. **Volume not changing**: Check that applications are in the correct lists
3. **Application not responding**: Restart the application

### Logs

The application prints status information to the console:
- `[INFO]`: General information
- `[WARNING]`: Non-critical issues
- `[ERROR]`: Error conditions

## License

This project is open source. See the license file for details.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## Changelog

For detailed version history and changes, see [CHANGELOG.md](CHANGELOG.md).

### Latest Version (1.1)
- **Auto-detection of new audio applications**: UI refreshes automatically every 5 seconds
- **Mutual exclusion validation**: Apps can only be in Priority OR Music lists
- **Enhanced input validation**: All configuration values validated and corrected automatically
- **Real-time feedback**: Immediate application of volume changes
- **Complete project restructure**: Organized code into modular packages
- **Enhanced UI**: Real-time value display on sliders with percentage indicators
- **Improved stability**: Fixed thread safety issues and initialization errors

### Previous Versions
- **Version 1.0**: Initial release with basic volume ducking functionality, multi-language support
