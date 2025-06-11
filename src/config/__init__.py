"""
Configuration module for AutoVolumeManager
"""

from .settings import load_config, save_config, create_config_template, DEFAULT_CONFIG
from .languages import get_language, get_available_languages, LANG

__all__ = [
    'load_config',
    'save_config', 
    'create_config_template',
    'DEFAULT_CONFIG',
    'get_language',
    'get_available_languages',
    'LANG'
]
