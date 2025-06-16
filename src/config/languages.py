"""
Language definitions for AutoVolumeManager
"""

LANG = {
    "en": {
        "title": "Auto Volume Manager",
        "priority": "Priority Apps",
        "music": "Music Apps",
        "vol_normal": "Normal Volume",
        "vol_ducked": "Lowered Volume",
        "peak": "Peak Threshold",
        "delay": "Restore Delay (s)",
        "fade_duration": "Fade Duration (s)",
        "show_hidden": "Show hidden apps",
        "hide": "Hide",
        "mode": "Appearance",
        "lang": "Language",
        "advanced_options": "Advanced Options",
        "basic_settings": "Basic Settings",
        "validation_info": "Note: Apps can only be in one list (Priority OR Music, not both)",
        "moved_to_priority": "moved to Priority Apps",
        "moved_to_music": "moved to Music Apps"
    },
    "es": {
        "title": "Gestor de Volumen Automático",
        "priority": "Apps Prioritarias",
        "music": "Apps de Música",
        "vol_normal": "Volumen normal",
        "vol_ducked": "Volumen reducido",
        "peak": "Umbral de sonido",
        "delay": "Retardo de restauración (s)",
        "fade_duration": "Duración del fade (s)",
        "show_hidden": "Mostrar apps ocultas",
        "hide": "Ocultar",
        "mode": "Apariencia",
        "lang": "Idioma",
        "advanced_options": "Opciones Avanzadas",
        "basic_settings": "Configuración Básica",
        "validation_info": "Nota: Las apps solo pueden estar en una lista (Prioritarias O Música, no ambas)",
        "moved_to_priority": "movida a Apps Prioritarias",
        "moved_to_music": "movida a Apps de Música"
    }
}

def get_language(lang_code: str) -> dict:
    """Get language dictionary for the specified language code"""
    return LANG.get(lang_code, LANG["en"])

def get_available_languages() -> list:
    """Get list of available language codes"""
    return list(LANG.keys())
