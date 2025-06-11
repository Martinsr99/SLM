"""
AutoVolumeManager - Main entry point
Automatic volume ducking application for priority audio
"""

import sys
import os
import customtkinter as ctk

# Add src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.ui.main_window import VolumeApp
from src.config.settings import create_config_template


def main():
    """Main application entry point"""
    # Create configuration template if it doesn't exist
    create_config_template()
    
    # Create and configure main window
    root = ctk.CTk()
    
    # Create application instance
    app = VolumeApp(root)
    
    # Configure window closing behavior
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    
    # Start the application
    try:
        root.mainloop()
    except KeyboardInterrupt:
        print("\n[INFO] Application interrupted by user")
        app.on_closing()
    except Exception as e:
        print(f"[ERROR] Application error: {e}")
        app.on_closing()


if __name__ == "__main__":
    main()
