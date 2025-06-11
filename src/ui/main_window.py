"""
Main window UI for AutoVolumeManager
"""
import threading
import customtkinter as ctk
from typing import Dict, Any, Callable, Optional

from ..config.settings import load_config, save_config
from ..config.languages import get_language, get_available_languages
from ..core.audio_utils import list_audio_apps
from ..core.volume_manager import VolumeManager


class VolumeApp:
    """Main application window and UI controller"""
    
    def __init__(self, root: ctk.CTk):
        """
        Initialize the main application window
        
        Args:
            root: The main CTk window
        """
        self.root = root
        self.config = load_config()
        self.lang = get_language(self.config["language"])
        
        # Configure appearance
        ctk.set_appearance_mode(self.config["appearance_mode"])
        ctk.set_default_color_theme("dark-blue")
        self.root.title(self.lang["title"])
        self.root.geometry("900x700")
        
        # Initialize variables
        self.volume_normal = ctk.DoubleVar(value=self.config["volume_normal"])
        self.volume_ducked = ctk.DoubleVar(value=self.config["volume_ducked"])
        self.peak_threshold = ctk.DoubleVar(value=self.config["peak_threshold"])
        self.restore_delay = ctk.DoubleVar(value=self.config.get("restore_delay", 3.0))
        self.show_all = ctk.BooleanVar(value=False)
        
        # UI components
        self.frame: Optional[ctk.CTkFrame] = None
        self.app_vars: Dict[str, tuple] = {}
        self.value_labels: Dict[str, tuple] = {}
        
        # Volume manager
        self.volume_manager: Optional[VolumeManager] = None
        
        # Initialize UI and start volume manager
        self.setup_ui()
        self.start_volume_manager()

    def setup_ui(self) -> None:
        """Setup the main UI components"""
        self.frame = ctk.CTkFrame(self.root)
        self.frame.pack(fill="both", expand=True, padx=20, pady=20)
        self.draw_ui()

    def draw_ui(self) -> None:
        """Draw/redraw the complete user interface"""
        if not self.frame:
            return
            
        # Clear existing widgets
        for widget in self.frame.winfo_children():
            widget.destroy()

        # Configure grid layout
        self.frame.grid_rowconfigure(0, weight=4)
        self.frame.grid_rowconfigure(1, weight=0)
        self.frame.grid_rowconfigure(2, weight=2)
        self.frame.grid_rowconfigure(3, weight=1)
        self.frame.grid_columnconfigure(0, weight=1)

        self._create_app_selection_area()
        self._create_show_hidden_checkbox()
        self._create_sliders_area()
        self._create_settings_area()

    def _create_app_selection_area(self) -> None:
        """Create the application selection area (top section)"""
        # Top scrollable areas
        top = ctk.CTkFrame(self.frame)
        top.grid(row=0, column=0, sticky="nsew", pady=(0, 10))
        top.grid_columnconfigure((0, 1), weight=1)

        apps = list_audio_apps()
        visible = [a for a in apps if self.show_all.get() or a not in self.config["ignored_apps"]]

        left = ctk.CTkScrollableFrame(top)
        right = ctk.CTkScrollableFrame(top)
        left.grid(row=0, column=0, sticky="nsew", padx=(0, 5))
        right.grid(row=0, column=1, sticky="nsew", padx=(5, 0))

        ctk.CTkLabel(left, text=self.lang["priority"], font=ctk.CTkFont(size=16, weight="bold")).pack(pady=6)
        ctk.CTkLabel(right, text=self.lang["music"], font=ctk.CTkFont(size=16, weight="bold")).pack(pady=6)

        self.app_vars = {}
        for app in visible:
            var_p = ctk.BooleanVar(value=app in self.config["priority_apps"])
            var_m = ctk.BooleanVar(value=app in self.config["music_apps"])
            self.app_vars[app] = (var_p, var_m)

            self._create_app_row(left, right, app, var_p, var_m)

    def _create_app_row(self, left_frame: ctk.CTkScrollableFrame, right_frame: ctk.CTkScrollableFrame, 
                       app: str, var_p: ctk.BooleanVar, var_m: ctk.BooleanVar) -> None:
        """Create a row for an application in both priority and music columns"""
        row_l = ctk.CTkFrame(left_frame)
        row_r = ctk.CTkFrame(right_frame)
        row_l.pack(fill="x", padx=6, pady=2)
        row_r.pack(fill="x", padx=6, pady=2)

        ctk.CTkCheckBox(row_l, text=app, variable=var_p, command=self.update_config).pack(side="left")
        ctk.CTkCheckBox(row_r, text=app, variable=var_m, command=self.update_config).pack(side="left")

        if self.show_all.get() and app in self.config["ignored_apps"]:
            btn = ctk.CTkButton(row_l, text="➕", width=32, command=lambda a=app: self.restore_app(a))
            btn.pack(side="right", padx=5)
            btn2 = ctk.CTkButton(row_r, text="➕", width=32, command=lambda a=app: self.restore_app(a))
            btn2.pack(side="right", padx=5)
        else:
            btn = ctk.CTkButton(row_l, text=self.lang["hide"], width=60, command=lambda a=app: self.hide_app(a))
            btn.pack(side="right", padx=5)
            btn2 = ctk.CTkButton(row_r, text=self.lang["hide"], width=60, command=lambda a=app: self.hide_app(a))
            btn2.pack(side="right", padx=5)

    def _create_show_hidden_checkbox(self) -> None:
        """Create the show hidden apps checkbox"""
        ctk.CTkCheckBox(
            self.frame, 
            text=self.lang["show_hidden"], 
            variable=self.show_all, 
            command=self.draw_ui,
            font=ctk.CTkFont(size=12)
        ).grid(row=1, column=0, pady=5)

    def _create_sliders_area(self) -> None:
        """Create the sliders configuration area"""
        sliders = ctk.CTkFrame(self.frame)
        sliders.grid(row=2, column=0, sticky="nsew", pady=10)
        sliders.grid_columnconfigure(0, weight=1)

        # Create labels to show current values
        self.value_labels = {}
        
        slider_configs = [
            ("vol_normal", self.lang["vol_normal"], self.volume_normal, 1, "%"),
            ("vol_ducked", self.lang["vol_ducked"], self.volume_ducked, 1, "%"),
            ("peak", self.lang["peak"], self.peak_threshold, 0.1, ""),
            ("delay", self.lang["delay"], self.restore_delay, 10, "s")
        ]

        for i, (key, label, var, maxv, unit) in enumerate(slider_configs):
            self._create_slider_row(sliders, i, key, label, var, maxv, unit)

    def _create_slider_row(self, parent: ctk.CTkFrame, row: int, key: str, label: str, 
                          var: ctk.DoubleVar, max_val: float, unit: str) -> None:
        """Create a single slider row with label and value display"""
        # Container frame for each slider
        slider_container = ctk.CTkFrame(parent)
        slider_container.grid(row=row, column=0, sticky="ew", padx=10, pady=5)
        slider_container.grid_columnconfigure(1, weight=1)
        
        # Label and value display
        label_frame = ctk.CTkFrame(slider_container)
        label_frame.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(5, 2))
        label_frame.grid_columnconfigure(1, weight=1)
        
        ctk.CTkLabel(label_frame, text=label, font=ctk.CTkFont(weight="bold")).grid(
            row=0, column=0, sticky="w", padx=5
        )
        
        # Value label
        value_text = self._format_value(var.get(), unit)
        value_label = ctk.CTkLabel(label_frame, text=value_text, font=ctk.CTkFont(size=12))
        value_label.grid(row=0, column=1, sticky="e", padx=5)
        self.value_labels[key] = (value_label, unit)
        
        # Slider
        slider = ctk.CTkSlider(
            slider_container, 
            from_=0, 
            to=max_val, 
            variable=var, 
            command=lambda val, k=key: self.update_slider_value(k, val)
        )
        slider.grid(row=1, column=0, columnspan=2, sticky="ew", padx=5, pady=(2, 5))

    def _create_settings_area(self) -> None:
        """Create the bottom settings area"""
        # Bottom configuration section
        bottom = ctk.CTkFrame(self.frame)
        bottom.grid(row=3, column=0, sticky="ew", pady=5)
        bottom.grid_columnconfigure((0, 1), weight=1)
        
        # Appearance section
        appearance_frame = ctk.CTkFrame(bottom)
        appearance_frame.grid(row=0, column=0, sticky="ew", padx=(5, 2.5), pady=5)
        
        ctk.CTkLabel(appearance_frame, text=self.lang["mode"], font=ctk.CTkFont(weight="bold")).pack(pady=(5, 2))
        current_mode = self.config.get("appearance_mode", "dark")
        mode_menu = ctk.CTkOptionMenu(appearance_frame, values=["dark", "light"], command=self.change_mode)
        mode_menu.set(current_mode)
        mode_menu.pack(pady=(0, 5))
        
        # Language section
        language_frame = ctk.CTkFrame(bottom)
        language_frame.grid(row=0, column=1, sticky="ew", padx=(2.5, 5), pady=5)
        
        ctk.CTkLabel(language_frame, text=self.lang["lang"], font=ctk.CTkFont(weight="bold")).pack(pady=(5, 2))
        current_lang = self.config.get("language", "en")
        lang_menu = ctk.CTkOptionMenu(language_frame, values=get_available_languages(), command=self.change_lang)
        lang_menu.set(current_lang)
        lang_menu.pack(pady=(0, 5))

    def _format_value(self, value: float, unit: str) -> str:
        """Format a value with its unit for display"""
        if unit == "%":
            return f"{int(value * 100)}{unit}"
        elif unit == "":
            return f"{value:.3f}{unit}"
        else:
            return f"{value:.1f}{unit}"

    def hide_app(self, app: str) -> None:
        """Hide an application from the interface"""
        if app not in self.config["ignored_apps"]:
            self.config["ignored_apps"].append(app)
            self.update_config()
            self.draw_ui()

    def restore_app(self, app: str) -> None:
        """Restore a hidden application to the interface"""
        if app in self.config["ignored_apps"]:
            self.config["ignored_apps"].remove(app)
            self.update_config()
            self.draw_ui()

    def update_slider_value(self, key: str, value: str) -> None:
        """Update the displayed value when slider changes"""
        if hasattr(self, 'value_labels') and key in self.value_labels:
            label, unit = self.value_labels[key]
            value_text = self._format_value(float(value), unit)
            label.configure(text=value_text)
        self.update_config()

    def update_config(self, _=None) -> None:
        """Update and save configuration, apply changes immediately"""
        config = self.get_config()
        save_config(config)
        
        # Apply changes immediately according to current state
        if self.volume_manager:
            if self.volume_manager.is_ducked:
                # If music is being ducked, apply new ducked volume immediately
                self.volume_manager.force_duck()
            else:
                # If music is at normal volume, apply new normal volume immediately
                self.volume_manager.force_restore()

    def change_mode(self, mode: str) -> None:
        """Change appearance mode"""
        self.config["appearance_mode"] = mode
        save_config(self.get_config())
        ctk.set_appearance_mode(mode)

    def change_lang(self, lang_code: str) -> None:
        """Change interface language"""
        self.config["language"] = lang_code
        self.lang = get_language(lang_code)
        save_config(self.get_config())
        self.draw_ui()

    def get_config(self) -> Dict[str, Any]:
        """Get current configuration from UI state"""
        # Create a thread-safe copy of app_vars to avoid "dictionary changed size during iteration"
        app_vars_copy = dict(self.app_vars)
        priority = [a for a, (p, _) in app_vars_copy.items() if p.get()]
        music = [a for a, (_, m) in app_vars_copy.items() if m.get()]
        
        return {
            "priority_apps": priority,
            "music_apps": music,
            "volume_normal": self.volume_normal.get(),
            "volume_ducked": self.volume_ducked.get(),
            "peak_threshold": self.peak_threshold.get(),
            "restore_delay": self.restore_delay.get(),
            "ignored_apps": self.config.get("ignored_apps", []),
            "appearance_mode": self.config["appearance_mode"],
            "language": self.config["language"]
        }

    def start_volume_manager(self) -> None:
        """Start the volume manager in a separate thread"""
        self.volume_manager = VolumeManager(self.get_config)
        threading.Thread(target=self.volume_manager.monitor_loop, daemon=True).start()

    def on_closing(self) -> None:
        """Handle application closing"""
        if self.volume_manager:
            self.volume_manager.stop()
        self.root.destroy()
