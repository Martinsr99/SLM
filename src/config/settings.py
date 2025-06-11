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
    
    # Validate and clean loaded configuration
    config = _validate_config(config)
    save_config(config)
    return config

def _validate_config(config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validate and clean configuration data
    
    Args:
        config: Configuration dictionary to validate
        
    Returns:
        Cleaned and validated configuration
    """
    # Ensure all required keys exist with proper types
    validated_config = DEFAULT_CONFIG.copy()
    
    # Validate numeric values
    for key in ["volume_normal", "volume_ducked", "peak_threshold"]:
        value = config.get(key, DEFAULT_CONFIG[key])
        if isinstance(value, (int, float)):
            validated_config[key] = max(0.0, min(1.0, float(value)))
        else:
            print(f"[WARNING] Invalid {key} value: {value}. Using default.")
            validated_config[key] = DEFAULT_CONFIG[key]
    
    # Validate restore delay
    restore_delay = config.get("restore_delay", DEFAULT_CONFIG["restore_delay"])
    if isinstance(restore_delay, (int, float)):
        validated_config["restore_delay"] = max(0.1, min(60.0, float(restore_delay)))
    else:
        print(f"[WARNING] Invalid restore_delay value: {restore_delay}. Using default.")
        validated_config["restore_delay"] = DEFAULT_CONFIG["restore_delay"]
    
    # Validate list fields
    for key in ["priority_apps", "music_apps", "ignored_apps"]:
        value = config.get(key, [])
        if isinstance(value, list):
            # Ensure all items are strings and remove duplicates
            validated_config[key] = list(set(str(item) for item in value if item))
        else:
            print(f"[WARNING] Invalid {key} value: {value}. Using empty list.")
            validated_config[key] = []
    
    # Remove apps that appear in both priority and music lists (priority wins)
    priority_set = set(validated_config["priority_apps"])
    music_set = set(validated_config["music_apps"])
    duplicates = priority_set & music_set
    
    if duplicates:
        print(f"[WARNING] Apps found in both priority and music lists: {duplicates}")
        print("[INFO] Keeping in priority list, removing from music list")
        validated_config["music_apps"] = [app for app in validated_config["music_apps"] 
                                         if app not in duplicates]
    
    # Validate string fields
    appearance_mode = config.get("appearance_mode", "dark")
    if appearance_mode in ["dark", "light"]:
        validated_config["appearance_mode"] = appearance_mode
    else:
        print(f"[WARNING] Invalid appearance_mode: {appearance_mode}. Using 'dark'.")
        validated_config["appearance_mode"] = "dark"
    
    language = config.get("language", "en")
    if language in ["en", "es"]:
        validated_config["language"] = language
    else:
        print(f"[WARNING] Invalid language: {language}. Using 'en'.")
        validated_config["language"] = "en"
    
    return validated_config

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
