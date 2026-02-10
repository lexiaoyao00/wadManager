import flet as ft
from widgets.mod_label import ModLabel,ModInfo
from widgets.nav_bar import NavBar
from pathlib import Path
from config import settings
from flet_router import router
from models import mod_manager

@ft.control
class HomeViewWidget(ft.Column):
    def init(self):
        self.expand = True

    def build(self):
        self.controls = [
            ft.Text("Welcome to the Home View!", size=30, weight=ft.FontWeight.BOLD),
        ]

@router.route('/')
class HomeView(ft.View):
    def init(self):
        self.scroll = ft.ScrollMode.AUTO
        self.route = '/'
        self._assets_path = Path(settings.load_mod_dir)

        self.gird_layout = ft.Row(
            wrap=True,
            spacing=10,
            run_spacing=10,
            scroll = ft.ScrollMode.AUTO,
        )
        mod_manager.load_mods(self._assets_path)
        mod_manager.organize_mods()

        for mod_info in mod_manager.mods.values():
            self.gird_layout.controls.append(ModLabel(mod_info))


    def build(self):

        self.controls = [
            NavBar(title='主页'),
            self.gird_layout
        ]