import flet as ft
from typing import Union
from schemas.mod_info import ModState, ModInfo,InstallState
from models import mod_manager
from pubsub import pub
from utils import EventTopic
import asyncio

@ft.control
class TitleText(ft.Text):
    """标题文本"""
    weight : ft.FontWeight = ft.FontWeight.BOLD
    size : int = 20

@ft.control
class AuthorText(ft.Text):
    """作者文本"""
    size : int = 15

@ft.control
class CoverImage(ft.Image):
    """封面图片"""
    border_radius : int = 10
    fit:ft.BoxFit = ft.BoxFit.FILL

@ft.control
class InstallStateChip(ft.Chip):
    """安装状态标签"""
    def __init__(self, install_state: InstallState = InstallState.UNINSTALLED):
        self.state = install_state
        super().__init__(label=self.state.value)

    def init(self):
        self.width = 100
        self.height = 30
        self.border_radius = 10
        self.margin = 5

    def build(self):

        if self.state == InstallState.INSTALLED:
            self.color = ft.Colors.GREEN_200

        elif self.state == InstallState.UNINSTALLED:
            self.color = ft.Colors.GREY_100



@ft.control
class ModContainer(ft.Container):
    def __init__(self,mod_path: str, state : ModState):
        self.mod_path = mod_path
        self.mod_info = mod_manager.mods.get(mod_path)
        self.state = state
        self.cover = self.mod_info.cover or "assets/img/10655689.jpg"
        self.title = self.mod_info.name or "未知名称"
        self.author = self.mod_info.author or "未知作者"


        pub.subscribe(self.update_mod_info, EventTopic.MOD_INFO_UPDATE.value)

        self.selected = False
        self.installed = False
        if self.state.install_state == InstallState.INSTALLED:
            self.installed = True
        super().__init__()

    def init(self):
        self.expand = True
        self.width = 200
        self.border_radius = 10
        self.border = ft.Border.all(width=2,color=ft.Colors.GREY_200)
        self.alignment = ft.Alignment.CENTER
        self.on_click = self._select
        self.on_hover = self._on_hover

    def build(self):
        self.cover_image = CoverImage(src=self.cover)
        self.title_text = TitleText(value=self.title)
        self.author_text = AuthorText(value=self.author)
        self.state_chip = InstallStateChip(install_state=self.state.install_state)

        self.content = ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            expand=True,
            controls=[
                self.cover_image,
                self.title_text,
                self.author_text,
                self.state_chip
            ]
        )

    def _on_hover(self, e:ft.HoverEvent):
        if self.selected:
            return
        if e.data:
            self.border = ft.Border.all(width=2,color=ft.Colors.BLACK)
            self.scale = 1.02
        else:
            self.border = ft.Border.all(width=2,color=ft.Colors.GREY)
            self.scale = 1.0



    def _select(self, e:ft.TapEvent):
        if self.selected:
            self.selected = False
            self.border = ft.Border.all(width=2,color=ft.Colors.BLACK)
        else:
            self.selected = True
            self.border = ft.Border.all(width=4,color=ft.Colors.BLUE)

    def _install_or_uninstall(self, e:ft.TapEvent):
        if self.installed:
            self._uninstall()
        else:
            self._install()

    def _install(self):
        self.installed = True
        self.state.install_state = InstallState.INSTALLED
        self.build()
        pub.sendMessage(EventTopic.MOD_INSTALL.value, mod_info=self.mod_info)

    def _uninstall(self):
        self.installed = False
        self.state.install_state = InstallState.UNINSTALLED
        self.build()
        pub.sendMessage(EventTopic.MOD_UNINSTALL.value, mod_info=self.mod_info)

    def update_mod_info(self, mod_path : str, mod_info : ModInfo):
        if mod_path == self.mod_path:
            self.title = mod_info.name or self.title
            self.author = mod_info.author or self.author
            self.cover = mod_info.cover or self.cover

            self.build()


@ft.control
class ModLabel(ft.ContextMenu):
    def __init__(self, mod_path : str,state : ModState):

        self.mod_path = mod_path
        self.state = state
        self.mod_container = ModContainer(self.mod_path, self.state)
        super().__init__(content=self.mod_container)

    def build(self):
        self.secondary_items = [
            ft.PopupMenuItem(content="安装/卸载", on_click=self._install_or_uninstall),
            ft.PopupMenuItem(content="详情", on_click=self._show_detail)
        ]
        self.secondary_trigger = ft.ContextMenuTrigger.DOWN,

    def _show_detail(self, e:ft.TapEvent):
        self.page.session.store.set('mod_path',self.mod_path)
        asyncio.create_task(self.page.push_route('/detail'))

    def _install_or_uninstall(self, e:ft.TapEvent):
        self.mod_container._install_or_uninstall(e)
        mod_manager.save_installed_mods()


    def install(self):
        self.mod_container._install()

    def uninstall(self):
        self.mod_container._uninstall()

    @property
    def selected(self):
        return self.mod_container.selected

    @selected.setter
    def selected(self, value):
        self.mod_container.selected = value

    @property
    def installed(self):
        return self.mod_container.installed

    @installed.setter
    def installed(self, value):
        self.mod_container.installed = value