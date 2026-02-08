import flet as ft
from config import settings

@ft.control
class DirView(ft.Row):
    def __init__(self, name : str, default_value : str = None):
        self._name = name
        self._default_value = default_value
        super().__init__()

    def init(self):
        self.alignment = ft.MainAxisAlignment.SPACE_BETWEEN
        self.expand = True

    def build(self):
        self.controls = [
            ft.TextField(label=self._name,
                         value=self._default_value or '',
                         border=ft.InputBorder.OUTLINE,
                         text_size=20,
                         width=300),
            ft.IconButton(icon=ft.Icons.CHECK,
                          icon_color=ft.Colors.BLACK,
                          on_click=self.on_check)
        ]

    def on_check(self, e:ft.Event[ft.IconButton]):
        print(e)

@ft.control
class SettingView(ft.Column):
    def init(self):
        self.expand = True
        self.scroll = ft.ScrollMode.AUTO
        self.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self.spacing = 10
        self.margin = 10


        self.controls = [
            DirView(name="下载目录:",default_value=settings.download_dir),
            DirView(name="数据目录:",default_value=settings.data_dir),
            DirView(name="临时目录:",default_value=settings.temp_dir),
        ]

