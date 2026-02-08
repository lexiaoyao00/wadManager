class AppState:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AppState, cls).__new__(cls)
            cls._instance.__init__()
        return cls._instance


    def __init__(self):
        self.game_path = "C:/Games/MyGame"
        self.mods = []
        self.version = "1.0.0"