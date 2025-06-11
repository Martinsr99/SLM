"""
Audio utilities for AutoVolumeManager
"""
from pycaw.pycaw import AudioUtilities, ISimpleAudioVolume, IAudioMeterInformation
from comtypes import CoInitialize
from typing import List, Set


def list_audio_apps() -> List[str]:
    """Get list of all audio applications currently running"""
    sessions = AudioUtilities.GetAllSessions()
    apps = set()
    for session in sessions:
        if session.Process:
            apps.add(session.Process.name().lower())
    return sorted(apps)


def initialize_com() -> None:
    """Initialize COM for audio operations"""
    CoInitialize()


def set_app_volume(app_name: str, volume: float) -> bool:
    """
    Set volume for a specific application
    
    Args:
        app_name: Name of the application (case insensitive)
        volume: Volume level (0.0 to 1.0)
        
    Returns:
        True if volume was set successfully, False otherwise
    """
    try:
        sessions = AudioUtilities.GetAllSessions()
        for session in sessions:
            if session.Process and session.Process.name().lower() == app_name.lower():
                volume_interface = session._ctl.QueryInterface(ISimpleAudioVolume)
                volume_interface.SetMasterVolume(volume, None)
                return True
    except Exception as e:
        print(f"[ERROR] Failed to set volume for {app_name}: {e}")
    return False


def get_app_peak_volume(app_name: str) -> float:
    """
    Get peak volume level for a specific application
    
    Args:
        app_name: Name of the application (case insensitive)
        
    Returns:
        Peak volume level (0.0 to 1.0), or 0.0 if not found or error
    """
    try:
        sessions = AudioUtilities.GetAllSessions()
        for session in sessions:
            if session.Process and session.Process.name().lower() == app_name.lower():
                meter = session._ctl.QueryInterface(IAudioMeterInformation)
                return meter.GetPeakValue()
    except Exception as e:
        print(f"[ERROR] Failed to get peak volume for {app_name}: {e}")
    return 0.0


def set_multiple_apps_volume(app_names: List[str], volume: float) -> int:
    """
    Set volume for multiple applications
    
    Args:
        app_names: List of application names
        volume: Volume level (0.0 to 1.0)
        
    Returns:
        Number of applications that had their volume set successfully
    """
    success_count = 0
    for app_name in app_names:
        if set_app_volume(app_name, volume):
            success_count += 1
    return success_count


def check_apps_audio_activity(app_names: List[str], threshold: float) -> List[str]:
    """
    Check which applications from the list have audio activity above threshold
    
    Args:
        app_names: List of application names to check
        threshold: Audio threshold (0.0 to 1.0)
        
    Returns:
        List of application names with audio activity above threshold
    """
    active_apps = []
    for app_name in app_names:
        peak = get_app_peak_volume(app_name)
        if peak > threshold:
            active_apps.append(app_name)
    return active_apps
