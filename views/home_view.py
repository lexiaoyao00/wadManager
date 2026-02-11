import flet as ft
from widgets.mod_label import ModLabel,ModInfo,ModState, InstallState
from widgets.nav_bar import NavBar
from pathlib import Path
from config import settings
from flet_router import router
from models import mod_manager
import asyncio

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
        self._assets_path = settings.mod_dir

        self.menu = ft.Row(
            alignment=ft.MainAxisAlignment.END,
            expand=True,
            controls=[
                ft.Button(content="安装选择", on_click=self.install_mods),
                ft.Button(content="卸载选择", on_click=self.uninstall_mods),
                ft.Button(content="加载模型", on_click=self.load_mods),
            ]
        )
        self.mod_gird = ft.Row(
            wrap=True,
            spacing=10,
            run_spacing=10,
            scroll = ft.ScrollMode.AUTO,
        )
        mod_manager.load_mods(self._assets_path)
        # if self._assets_path != settings.mod_dir:
        #     mod_manager.organize_mods()
        mod_manager.load_installed_mods()

        self.show_mods_info()


    def show_mods_info(self):
        self.mod_gird.controls.clear()
        for mod_path, mod_info in mod_manager.mods.items():
            state = ModState()
            if mod_info in mod_manager.installed_mods_info.installed_mods:
                state.install_state = InstallState.INSTALLED
            self.mod_gird.controls.append(ModLabel(mod_path, state))

    def build(self):

        self.controls = [
            NavBar(title='主页'),
            ft.Column(
                expand=True,
                controls=[
                    self.menu,
                    self.mod_gird,
                ],
                margin=10,
            ),

        ]

    def install_mods(self, e):
        selected_mods = [mod for mod in self.mod_gird.controls if isinstance(mod, ModLabel) and mod.selected == True]
        if len(selected_mods) == 0:
            self.page.show_dialog(ft.AlertDialog(title='警告', content=ft.Text('请选择要安装的模型')))
            return

        for mod in selected_mods:
            mod.install()
        mod_manager.save_installed_mods()


    def uninstall_mods(self, e):
        selected_mods = [mod for mod in self.mod_gird.controls if isinstance(mod, ModLabel) and mod.selected == True]
        if len(selected_mods) == 0:
            self.page.show_dialog(ft.AlertDialog(title='警告', content=ft.Text('请选择要安装的模型')))
            return

        for mod in selected_mods:
            mod.uninstall()
        mod_manager.save_installed_mods()



    async def load_mods(self, e):
        selected_path = await ft.FilePicker().get_directory_path(dialog_title='选择模型目录')

        if selected_path is None:
            return

        if selected_path == self._assets_path:
            self.page.show_dialog(ft.AlertDialog(title='警告', content=ft.Text('当前目录为工具存放模型的目录，无需重复加载')))
            return

        mod_manager.load_mods(selected_path)
        mod_manager.organize_mods()
        self.show_mods_info()
        self.page.update()


