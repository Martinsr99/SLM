"""
Core functionality module for AutoVolumeManager
"""

from .audio_utils import (
    list_audio_apps,
    initialize_com,
    set_app_volume,
    get_app_peak_volume,
    set_multiple_apps_volume,
    check_apps_audio_activity
)
from .volume_manager import VolumeManager

__all__ = [
    'list_audio_apps',
    'initialize_com',
    'set_app_volume',
    'get_app_peak_volume',
    'set_multiple_apps_volume',
    'check_apps_audio_activity',
    'VolumeManager'
]
