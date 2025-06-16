"""
Audio utilities for AutoVolumeManager
"""
from pycaw.pycaw import AudioUtilities, ISimpleAudioVolume, IAudioMeterInformation
from comtypes import CoInitialize
from typing import List, Set
import time
import threading


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


def get_app_current_volume(app_name: str) -> float:
    """
    Get current volume level for a specific application
    
    Args:
        app_name: Name of the application (case insensitive)
        
    Returns:
        Current volume level (0.0 to 1.0), or 0.0 if not found or error
    """
    try:
        sessions = AudioUtilities.GetAllSessions()
        for session in sessions:
            if session.Process and session.Process.name().lower() == app_name.lower():
                volume_interface = session._ctl.QueryInterface(ISimpleAudioVolume)
                return volume_interface.GetMasterVolume()
    except Exception as e:
        print(f"[ERROR] Failed to get current volume for {app_name}: {e}")
    return 0.0


def fade_app_volume(app_name: str, start_volume: float, end_volume: float, duration: float = 0.5) -> None:
    """
    Fade volume for a specific application from start to end volume
    
    Args:
        app_name: Name of the application (case insensitive)
        start_volume: Starting volume level (0.0 to 1.0)
        end_volume: Ending volume level (0.0 to 1.0)
        duration: Duration of fade in seconds (default 0.5)
    """
    def fade_worker():
        try:
            steps = 20  # Number of steps for smooth fade
            step_duration = duration / steps
            volume_step = (end_volume - start_volume) / steps
            
            for i in range(steps + 1):
                current_volume = start_volume + (volume_step * i)
                current_volume = max(0.0, min(1.0, current_volume))  # Clamp to valid range
                
                if set_app_volume(app_name, current_volume):
                    if i < steps:  # Don't sleep after the last step
                        time.sleep(step_duration)
                else:
                    # If we can't set volume, break out of the loop
                    break
                    
        except Exception as e:
            print(f"[ERROR] Failed to fade volume for {app_name}: {e}")
    
    # Run fade in a separate thread to avoid blocking
    fade_thread = threading.Thread(target=fade_worker, daemon=True)
    fade_thread.start()


def fade_multiple_apps_volume(app_names: List[str], start_volume: float, end_volume: float, duration: float = 0.5) -> int:
    """
    Fade volume for multiple applications
    
    Args:
        app_names: List of application names
        start_volume: Starting volume level (0.0 to 1.0)
        end_volume: Ending volume level (0.0 to 1.0)
        duration: Duration of fade in seconds (default 0.5)
        
    Returns:
        Number of applications that started fading successfully
    """
    success_count = 0
    for app_name in app_names:
        # Check if app exists before starting fade
        current_vol = get_app_current_volume(app_name)
        if current_vol >= 0:  # App exists
            fade_app_volume(app_name, start_volume, end_volume, duration)
            success_count += 1
    return success_count
