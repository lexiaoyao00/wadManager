import flet as ft
from widgets.mod_label import ModLabel,ModInfo,ModState, InstallState
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
        self._assets_path = settings.load_mod_dir

        self.menu = ft.Row(
            alignment=ft.MainAxisAlignment.END,
            controls=[
                ft.Button(content="安装选择")
            ]
        )
        self.mod_gird = ft.Row(
            wrap=True,
            spacing=10,
            run_spacing=10,
            scroll = ft.ScrollMode.AUTO,
        )
        mod_manager.load_mods(self._assets_path)
        if self._assets_path != settings.mod_dir:
            mod_manager.organize_mods()
        mod_manager.load_installed_mods()

        for mod_info in mod_manager.mods.values():
            state = ModState()
            if mod_info in mod_manager.installed_mods_info.installed_mods:
                state.install_state = InstallState.INSTALLED

            self.mod_gird.controls.append(ModLabel(mod_info, state))


    def build(self):

        self.controls = [
            NavBar(title='主页'),
            self.mod_gird
        ]

    def _install_selected(self, e:ft.Event[ft.Button]):
        for mod_label  in self.mod_gird.controls:
            if mod_label.selected:
                mod_label.mod_info.install()
                mod_label.selected = False