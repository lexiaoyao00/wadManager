import flet as ft
from config import settings
from widgets.nav_bar import NavBar
from flet_router import router
from pathlib import Path

@ft.control
class DirViewWidget(ft.Row):
    name : str = ""
    default_value : str = ""
    # TODO: 只要使用expand就会导致控件异常
    def init(self):
        self.dir_tf = ft.TextField(label=self.name,
                    value=self.default_value,
                    border=ft.InputBorder.OUTLINE,
                    text_size=20,
                    width=300,
                    # expand=1,
                    )

        self.select_btn = ft.IconButton(icon=ft.Icons.FOLDER_OPEN,tooltip='选择目录',on_click=self.on_select)
        self.expand = True

        self.controls = [
            self.dir_tf,
            self.select_btn
        ]

    async def on_select(self, e:ft.Event[ft.ElevatedButton]):
        if not Path(self.dir_tf.value).exists():
                Path(self.dir_tf.value).mkdir(parents=True)
        path = await ft.FilePicker().get_directory_path(initial_directory=self.dir_tf.value)
        self.dir_tf.value = path

@ft.control
class SettingViewWidget(ft.Column):
    def init(self):
        self.expand = True
        self.scroll = ft.ScrollMode.AUTO
        self.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self.spacing = 10
        self.margin = 10


    def build(self):
        tf = ft.TextField(label='test',
                         value='',
                         border=ft.InputBorder.OUTLINE,
                         text_size=20,
                         expand=1)
        btn = ft.IconButton(icon=ft.Icons.FOLDER_OPEN,tooltip='选择目录')
        self.controls = [
            DirViewWidget(name="下载目录:",default_value=settings.download_dir),
            DirViewWidget(name="数据目录:",default_value=settings.data_dir),
            DirViewWidget(name="临时目录:",default_value=settings.temp_dir),
            DirViewWidget(name="模型存放目录:",default_value=settings.mod_dir),
            DirViewWidget(name="输出目录:",default_value=settings.output_dir),
        ]
@router.route('/settings')
class SettingView(ft.View):
    def init(self):
        self.route = '/settings'
        self.controls = [
            NavBar(title='设置'),
            SettingViewWidget()
            ]

