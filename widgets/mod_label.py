import flet as ft
from typing import Union
from schemas.mod_info import InstallState, ModInfo
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
        if self.state == InstallState.INSTALLING:
            self.color = ft.Colors.YELLOW_100
        elif self.state == InstallState.INSTALLED:
            self.color = ft.Colors.GREEN_200
        elif self.state == InstallState.UNINSTALLING:
            self.color = ft.Colors.RED_100
        elif self.state == InstallState.UNINSTALLED:
            self.color = ft.Colors.GREY_100



@ft.control
class ModContainer(ft.Container):
    def __init__(self,mod_info: ModInfo):

        cover = mod_info.cover or "assets/img/10655689.jpg"
        title = mod_info.name or "未知名称"
        author = mod_info.author or "未知作者"

        state = mod_info.state or InstallState.UNINSTALLED
        self.cover_image = CoverImage(src=cover,width=200)
        self.title_text = TitleText(value=title)
        self.author_text = AuthorText(value=author)
        self.state_chip = InstallStateChip(install_state=state)
        super().__init__()

    def init(self):
        self.expand = True
        self.width = 200
        self.border_radius = 10
        self.border = ft.Border.all(width=2,color=ft.Colors.GREY_200)
        self.alignment = ft.Alignment.CENTER

    def build(self):
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

    def change_info(self,cover : Union[str,bytes] = None,
                    title : str = None,
                    author : str = None,
                    state : InstallState = None):
        self.cover_image.src = cover or self.cover_image.src
        self.title_text.value = title or self.title_text.value
        self.author_text.value = author or self.author_text.value
        self.state_chip = InstallStateChip(install_state=state) if state else self.state_chip.state
        self.build()

@ft.control
class ModLabel(ft.GestureDetector):
    def __init__(self, mod_info : ModInfo):

        self.mod_info = mod_info
        self._mod_container = ModContainer(self.mod_info)
        self.selected = False
        self.installed = False
        if self.mod_info.state == InstallState.INSTALLED:
            self.installed = True

        super().__init__()

    def init(self):
        self.width = self._mod_container.width
        self.height = self._mod_container.height
        self.content = self._mod_container
        self.tooltip = self.mod_info.description
        self.on_enter = self._on_enter
        self.on_exit = self._on_exit
        self.on_tap = self._select
        # self.on_double_tap = self._install

    def _on_exit(self, e:ft.PointerEvent):
        if self.selected:
            return

        self._mod_container.border = ft.Border.all(width=2,color=ft.Colors.GREY)
        self.scale = 1.0

    def _on_enter(self, e:ft.PointerEvent):
        if self.selected:
            return
        self._mod_container.border = ft.Border.all(width=2,color=ft.Colors.BLACK)
        self.scale = 1.02



    def _select(self, e:ft.TapEvent):
        if self.selected:
            self.selected = False
            self._mod_container.border = ft.Border.all(width=2,color=ft.Colors.GREY)
        else:
            self.selected = True
            self._mod_container.border = ft.Border.all(width=4,color=ft.Colors.BLUE)


    def _install(self, e:ft.TapEvent):
        self.installed = not self.installed
        current_state = InstallState.INSTALLED if self.installed else InstallState.UNINSTALLED
        self._mod_container.change_info(state = current_state)