

__all__ = [
    "settings",
    "load_settings",
    "save_settings",
    "BaseSettings",
]


from config.setting import load_settings,save_settings,BaseSettings

settings = load_settings()
