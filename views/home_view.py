import flet as ft
from widgets.mod_label import ModLabel,ModInfo,ModState, InstallState
from widgets.nav_bar import NavBar
from typing import Dict, List
from config import settings
from flet_router import router
from models import mod_manager
from pubsub import pub
from utils import EventTopic
import asyncio

@ft.control
class SearchBar(ft.Row):

    def init(self):
        self.alignment=ft.MainAxisAlignment.END
        self.margin = 10

        self._tf_search_kw = ft.TextField(label="搜索", width=200, on_submit=self.search_mods)
        self._btn_search = ft.ElevatedButton(content="清除搜索", on_click=self.clear_search)

    def build(self):
        self.controls=[
            self._tf_search_kw,
            self._btn_search,
        ]

    def clear_search(self, e):
        pub.sendMessage(EventTopic.SEARCH_MOD.value)

    def search_mods(self, e):
        pub.sendMessage(EventTopic.SEARCH_MOD.value, keyword=self._tf_search_kw.value)


@ft.control
class HomeMenu(ft.Row):

    def init(self):
        self.alignment=ft.MainAxisAlignment.END
        self.margin = 10

    def build(self):
        self.controls=[
            SearchBar(),
            ft.Button(content="安装选择", on_click=lambda _ : pub.sendMessage(EventTopic.INSTALL_SELECTED_MOD.value)),
            ft.Button(content="卸载选择", on_click=lambda _ : pub.sendMessage(EventTopic.UNINSTALL_SELECTED_MOD.value)),
            ft.Button(content="加载模型", on_click=lambda _ : pub.sendMessage(EventTopic.LOAD_MOD.value)),
        ]


@ft.control
class ModViewWidget(ft.Row):
    def init(self):
        self._assets_path = settings.mod_dir
        mod_manager.init_load(self._assets_path)
        self._subscribe_topic()

        self.wrap=True
        self.expand=True
        self.spacing=10
        self.run_spacing=10
        self.scroll = ft.ScrollMode.AUTO

    def _subscribe_topic(self):
        pub.subscribe(self.install_selected_mods, EventTopic.INSTALL_SELECTED_MOD.value)
        pub.subscribe(self.uninstall_selected_mods, EventTopic.UNINSTALL_SELECTED_MOD.value)
        pub.subscribe(self.load_mods, EventTopic.LOAD_MOD.value)
        pub.subscribe(self.show_search_result, EventTopic.SERACH_FINISHED.value)

    def build(self):
        self.show_mods_info()

    def show_search_result(self, result : Dict[str, ModInfo] = None):
        self.show_mods_info(mods=result)

    def show_mods_info(self, mods : Dict[str, ModInfo] = None, installed_mods : List[ModInfo] = None):
        if mods is None:
            mods = mod_manager.mods

        installed_mods = installed_mods or mod_manager.installed_mods_info.installed_mods

        self.controls.clear()
        for mod_path, mod_info in mods.items():
            state = ModState()
            if installed_mods and mod_info in installed_mods:
                state.install_state = InstallState.INSTALLED
            self.controls.append(ModLabel(mod_path, state))

        self.update()


    def install_selected_mods(self):
        selected_mods = [mod for mod in self.controls if isinstance(mod, ModLabel) and mod.selected == True]
        if len(selected_mods) == 0:
            self.page.show_dialog(ft.AlertDialog(title='警告', content=ft.Text('请选择要安装的模型')))
            return

        for mod in selected_mods:
            mod.install()
        mod_manager.save_installed_mods()


    def uninstall_selected_mods(self):
        selected_mods = [mod for mod in self.controls if isinstance(mod, ModLabel) and mod.selected == True]
        if len(selected_mods) == 0:
            self.page.show_dialog(ft.AlertDialog(title='警告', content=ft.Text('请选择要安装的模型')))
            return

        for mod in selected_mods:
            mod.uninstall()
        mod_manager.save_installed_mods()

    def load_mods(self):
        asyncio.create_task(self._load_mods())

    async def _load_mods(self):
        selected_path = await ft.FilePicker().get_directory_path(dialog_title='选择模型目录')

        if selected_path is None:
            return

        if selected_path == settings.mod_dir:
            self.page.show_dialog(ft.AlertDialog(title='警告', content=ft.Text('当前目录为工具存放模型的目录，无需重复加载')))
            return

        mod_manager.load_mods(selected_path)
        failed =  mod_manager.organize_mods(move=True)
        self.show_mods_info()
        if len(failed) > 0:
            alert = ft.AlertDialog(title='警告', content=ft.Text(f'以下模型已经存在，加载失败，请修改名称或者手动覆盖'))
            self.page.show_dialog(alert)
        self.page.update()



@router.route('/')
class HomeView(ft.View):

    def build(self):
        self.controls = [
            NavBar(title='主页'),
            HomeMenu(),
            ModViewWidget(),
        ]



