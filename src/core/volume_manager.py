"""
Volume Manager core functionality for AutoVolumeManager
"""
import time
from typing import Dict, Any, Callable
from .audio_utils import (
    initialize_com, 
    set_multiple_apps_volume, 
    check_apps_audio_activity,
    get_app_peak_volume,
    get_app_current_volume,
    fade_multiple_apps_volume
)


class VolumeManager:
    """
    Core volume management class that handles audio ducking logic
    """
    
    def __init__(self, get_config_func: Callable[[], Dict[str, Any]]):
        """
        Initialize VolumeManager
        
        Args:
            get_config_func: Function that returns current configuration
        """
        self.get_config = get_config_func
        self.is_ducked = False
        self.last_priority_time = time.time()
        self._running = False

    def duck_music(self) -> None:
        """Lower volume of music applications with fade out"""
        config = self.get_config()
        music_apps = config.get("music_apps", [])
        volume_ducked = config.get("volume_ducked", 0.2)
        fade_out_duration = config.get("fade_out_duration", 0.2)  # Fade out más rápido
        
        # Validate inputs
        if not music_apps or not isinstance(music_apps, list):
            return
            
        if not isinstance(volume_ducked, (int, float)) or volume_ducked < 0 or volume_ducked > 1:
            print(f"[WARNING] Invalid ducked volume: {volume_ducked}, using default")
            volume_ducked = 0.2
            
        if not isinstance(fade_out_duration, (int, float)) or fade_out_duration < 0.1 or fade_out_duration > 2.0:
            print(f"[WARNING] Invalid fade out duration: {fade_out_duration}, using default")
            fade_out_duration = 0.2
            
        # Filter out invalid app names
        valid_apps = [app for app in music_apps if app and isinstance(app, str)]
        
        if valid_apps:
            # Get current volume of first app to use as starting point
            start_volume = 1.0  # Default assumption
            if valid_apps:
                current_vol = get_app_current_volume(valid_apps[0])
                if current_vol > 0:
                    start_volume = current_vol
            
            success_count = fade_multiple_apps_volume(valid_apps, start_volume, volume_ducked, fade_out_duration)
            if success_count > 0:
                print(f"[INFO] Fading down {success_count} music app(s) to {volume_ducked:.1f}")
            elif len(valid_apps) > 0:
                print(f"[WARNING] Failed to fade any of {len(valid_apps)} music apps")

    def restore_music(self) -> None:
        """Restore normal volume of music applications with fade in"""
        config = self.get_config()
        music_apps = config.get("music_apps", [])
        volume_normal = config.get("volume_normal", 1.0)
        fade_in_duration = config.get("fade_in_duration", 0.4)  # Fade in más lento
        
        # Validate inputs
        if not music_apps or not isinstance(music_apps, list):
            return
            
        if not isinstance(volume_normal, (int, float)) or volume_normal < 0 or volume_normal > 1:
            print(f"[WARNING] Invalid normal volume: {volume_normal}, using default")
            volume_normal = 1.0
            
        if not isinstance(fade_in_duration, (int, float)) or fade_in_duration < 0.1 or fade_in_duration > 2.0:
            print(f"[WARNING] Invalid fade in duration: {fade_in_duration}, using default")
            fade_in_duration = 0.4
            
        # Filter out invalid app names
        valid_apps = [app for app in music_apps if app and isinstance(app, str)]
        
        if valid_apps:
            # Get current volume of first app to use as starting point
            start_volume = 0.2  # Default assumption (ducked volume)
            if valid_apps:
                current_vol = get_app_current_volume(valid_apps[0])
                if current_vol >= 0:
                    start_volume = current_vol
            
            success_count = fade_multiple_apps_volume(valid_apps, start_volume, volume_normal, fade_in_duration)
            if success_count > 0:
                print(f"[INFO] Fading up {success_count} music app(s) to {volume_normal:.1f}")
            elif len(valid_apps) > 0:
                print(f"[WARNING] Failed to fade any of {len(valid_apps)} music apps")

    def check_priority_audio(self) -> bool:
        """
        Check if any priority applications have audio activity above threshold
        
        Returns:
            True if priority audio is detected, False otherwise
        """
        config = self.get_config()
        priority_apps = config.get("priority_apps", [])
        peak_threshold = config.get("peak_threshold", 0.01)
        
        # Validate inputs
        if not priority_apps or not isinstance(priority_apps, list):
            return False
            
        if not isinstance(peak_threshold, (int, float)) or peak_threshold <= 0:
            print(f"[WARNING] Invalid peak threshold: {peak_threshold}, using default")
            peak_threshold = 0.01
            
        for app_name in priority_apps:
            if not app_name or not isinstance(app_name, str):
                continue
                
            peak = get_app_peak_volume(app_name)
            if peak > peak_threshold:
                print(f"[INFO] Audio detected in {app_name} (peak={peak:.2f})")
                return True
        
        return False

    def monitor_loop(self) -> None:
        """
        Main monitoring loop that handles volume ducking logic
        This method runs continuously until stopped
        """
        initialize_com()
        print("[INFO] Starting monitor loop...")
        self._running = True
        
        try:
            while self._running:
                config = self.get_config()
                restore_delay = config.get("restore_delay", 3.0)
                
                if self.check_priority_audio():
                    self.last_priority_time = time.time()
                    if not self.is_ducked:
                        print("[INFO] Ducking music")
                        self.duck_music()
                        self.is_ducked = True
                else:
                    if self.is_ducked and (time.time() - self.last_priority_time > restore_delay):
                        print("[INFO] Restoring music")
                        self.restore_music()
                        self.is_ducked = False
                
                time.sleep(0.5)
                
        except KeyboardInterrupt:
            print("[INFO] Monitor loop interrupted by user")
        except Exception as e:
            print(f"[ERROR] Monitor loop error: {e}")
        finally:
            self.stop()

    def stop(self) -> None:
        """Stop the monitoring loop"""
        self._running = False
        if self.is_ducked:
            print("[INFO] Restoring music before exit")
            self.restore_music()
            self.is_ducked = False
        print("[INFO] Volume manager stopped")

    def force_duck(self) -> None:
        """Force duck music applications (for immediate config changes)"""
        if self.is_ducked:
            self.duck_music()

    def force_restore(self) -> None:
        """Force restore music applications (for immediate config changes)"""
        if not self.is_ducked:
            self.restore_music()

    def get_status(self) -> Dict[str, Any]:
        """
        Get current status of the volume manager
        
        Returns:
            Dictionary with current status information
        """
        return {
            "is_ducked": self.is_ducked,
            "is_running": self._running,
            "last_priority_time": self.last_priority_time,
            "time_since_last_priority": time.time() - self.last_priority_time
        }
