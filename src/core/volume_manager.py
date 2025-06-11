"""
Volume Manager core functionality for AutoVolumeManager
"""
import time
from typing import Dict, Any, Callable
from .audio_utils import (
    initialize_com, 
    set_multiple_apps_volume, 
    check_apps_audio_activity,
    get_app_peak_volume
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
        """Lower volume of music applications"""
        config = self.get_config()
        music_apps = config.get("music_apps", [])
        volume_ducked = config.get("volume_ducked", 0.2)
        
        if music_apps:
            success_count = set_multiple_apps_volume(music_apps, volume_ducked)
            if success_count > 0:
                print(f"[INFO] Ducked {success_count} music app(s)")

    def restore_music(self) -> None:
        """Restore normal volume of music applications"""
        config = self.get_config()
        music_apps = config.get("music_apps", [])
        volume_normal = config.get("volume_normal", 1.0)
        
        if music_apps:
            success_count = set_multiple_apps_volume(music_apps, volume_normal)
            if success_count > 0:
                print(f"[INFO] Restored {success_count} music app(s)")

    def check_priority_audio(self) -> bool:
        """
        Check if any priority applications have audio activity above threshold
        
        Returns:
            True if priority audio is detected, False otherwise
        """
        config = self.get_config()
        priority_apps = config.get("priority_apps", [])
        peak_threshold = config.get("peak_threshold", 0.01)
        
        if not priority_apps:
            return False
            
        for app_name in priority_apps:
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
