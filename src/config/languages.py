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
        "show_hidden": "Show hidden apps",
        "hide": "Hide",
        "mode": "Appearance",
        "lang": "Language"
    },
    "es": {
        "title": "Gestor de Volumen Automático",
        "priority": "Apps Prioritarias",
        "music": "Apps de Música",
        "vol_normal": "Volumen normal",
        "vol_ducked": "Volumen reducido",
        "peak": "Umbral de sonido",
        "delay": "Retardo de restauración (s)",
        "show_hidden": "Mostrar apps ocultas",
        "hide": "Ocultar",
        "mode": "Apariencia",
        "lang": "Idioma"
    }
}

def get_language(lang_code: str) -> dict:
    """Get language dictionary for the specified language code"""
    return LANG.get(lang_code, LANG["en"])

def get_available_languages() -> list:
    """Get list of available language codes"""
    return list(LANG.keys())
