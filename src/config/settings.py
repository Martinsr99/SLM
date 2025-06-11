"""
Configuration management for AutoVolumeManager
"""
import json
import os
from typing import Dict, Any

CONFIG_FILE = "config.json"
CONFIG_TEMPLATE_FILE = "config.template.json"

DEFAULT_CONFIG = {
    "volume_normal": 1.0,
    "volume_ducked": 0.15,
    "peak_threshold": 0.01,
    "restore_delay": 1.0,
    "priority_apps": [],
    "music_apps": [],
    "ignored_apps": [],
    "appearance_mode": "dark",
    "language": "en"
}

def load_config() -> Dict[str, Any]:
    """Load configuration from file, create if doesn't exist"""
    config = DEFAULT_CONFIG.copy()
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                user_config = json.load(f)
                config.update(user_config)
        except (json.JSONDecodeError, FileNotFoundError) as e:
            print(f"[WARNING] Error loading config: {e}. Using defaults.")
    
    save_config(config)
    return config

def save_config(config: Dict[str, Any]) -> None:
    """Save configuration to file"""
    try:
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"[ERROR] Failed to save config: {e}")

def create_config_template() -> None:
    """Create a template configuration file"""
    template_config = DEFAULT_CONFIG.copy()
    template_config.update({
        "_comment": "AutoVolumeManager Configuration Template",
        "_description": {
            "volume_normal": "Normal volume level (0.0 to 1.0)",
            "volume_ducked": "Reduced volume level when priority audio is detected (0.0 to 1.0)",
            "peak_threshold": "Audio peak threshold to trigger ducking (0.0 to 1.0)",
            "restore_delay": "Delay in seconds before restoring normal volume",
            "priority_apps": "List of applications that trigger volume ducking",
            "music_apps": "List of music applications to be ducked",
            "ignored_apps": "List of applications to hide from the interface",
            "appearance_mode": "UI appearance mode: 'dark' or 'light'",
            "language": "Interface language: 'en' or 'es'"
        }
    })
    
    try:
        with open(CONFIG_TEMPLATE_FILE, "w", encoding="utf-8") as f:
            json.dump(template_config, f, indent=4, ensure_ascii=False)
        print(f"[INFO] Configuration template created: {CONFIG_TEMPLATE_FILE}")
    except Exception as e:
        print(f"[ERROR] Failed to create config template: {e}")
