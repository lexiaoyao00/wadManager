import flet as ft
from widgets.mod_label import ModLabel,ModInfo,ModState, InstallState
from widgets.nav_bar import NavBar
from pathlib import Path
from config import settings
from flet_router import router
from models import mod_manager
from loguru import logger
from utils import judge_file_type,FileType,EventTopic
from schemas.mod_info import ModCategory
import json
from typing import Dict,List
from pubsub import pub

MOD_TAG_COLORS : Dict[ModCategory,ft.Colors] = {
    ModCategory.SKIN : ft.Colors.AMBER_200,
    ModCategory.MAPS : ft.Colors.BLUE_200,
    ModCategory.MEMES : ft.Colors.GREEN_200,
    ModCategory.TFT : ft.Colors.RED_200,
    ModCategory.UI : ft.Colors.PURPLE_200,
    ModCategory.AUDIO : ft.Colors.YELLOW_200,
    ModCategory.VTUBER : ft.Colors.PINK_200,
    ModCategory.OTHER : ft.Colors.GREY_200,
}

@ft.control
class TagPicker(ft.Column):

    def __init__(self, selected_tags: List[ModCategory] = None):

        self.selected_tags : List[ModCategory] = selected_tags or []

        super().__init__()

    def init(self):
        self.tag_row = ft.Row(wrap=True,spacing=5)
        for tag in self.selected_tags:
            self.add_tag_chip(tag)

        self.suggestion_list = ft.Column(visible=False, spacing=2)

        self.input_field = ft.TextField(
            label="输入或选择类型",
            width=self.width,
            autofocus=False,
            on_change=self.on_input_change,
            on_submit=self.on_submit,
        )

    def build(self):
        self.controls = [
            self.tag_row,
            self.input_field,
            self.suggestion_list,
        ]

    def on_input_change(self, e:ft.Event[ft.TextField]):
        query = e.control.value.strip().lower()
        self.suggestion_list.controls.clear()

        if not query:
            self.suggestion_list.visible = False
        else:
            # 注意：这里从 Enum 取名字的值进行匹配
            matches = [
                tag for tag in MOD_TAG_COLORS.keys()
                if tag.value.lower().startswith(query)
                and tag not in self.selected_tags
            ]

            if matches:
                self.suggestion_list.visible = True
                for tag in matches:
                    self.suggestion_list.controls.append(
                        ft.ElevatedButton(tag.value, on_click=lambda e, t=tag: self.add_tag(t))
                    )
            else:
                self.suggestion_list.visible = False

        self.update()

    def on_submit(self, e:ft.Event[ft.TextField]):
        text = e.control.value.strip()
        if text:
            # 如果输入匹配现有枚举成员，则用枚举成员，否则可选：支持自定义
            match = next((tag for tag in MOD_TAG_COLORS.keys() if tag.value.lower() == text.lower()), None)
            if match:
                self.add_tag(match)
            # 如果你不希望用户输入自定义值，则 else 可忽略掉。

    def add_tag(self, tag: ModCategory):
        if tag in self.selected_tags:
            self.input_field.value = ""
            self.suggestion_list.visible = False
            self.update()
            return

        self.selected_tags.append(tag)

        self.add_tag_chip(tag)
        self.input_field.value = ""
        self.suggestion_list.visible = False
        self.update()

    def add_tag_chip(self, tag: ModCategory):
        chip_color = MOD_TAG_COLORS.get(tag, ft.Colors.GREY_300)

        chip = ft.Chip(
            label=ft.Text(tag.value),  # 显示枚举的值
            bgcolor=chip_color,
            on_delete=lambda e, t=tag: self.remove_tag(t),
        )
        self.tag_row.controls.append(chip)

    def remove_tag(self, tag: ModCategory):
        self.selected_tags.remove(tag)
        self.tag_row.controls[:] = [
            chip for chip in self.tag_row.controls if chip.label.value != tag.value
        ]
        self.update()

    def get_tags(self) -> list[ModCategory]:
        """返回当前选中的枚举成员列表"""
        return self.selected_tags.copy()



@ft.control
class DetailList(ft.Column):
    def __init__(self, mod_path: str):
        self.mod_path = mod_path
        super().__init__()

    def init(self):
        self.scroll = ft.ScrollMode.AUTO
        self.expand = True

    def build(self):
        self.mod_info = mod_manager.mods.get(self.mod_path)
        self.file_path_tf = ft.TextField(label="文件路径", value=self.mod_info.file_path,read_only=True,expand=True)
        self.name_tf = ft.TextField(label="名称", value=self.mod_info.name,expand=True)
        self.author_tf = ft.TextField(label="作者", value=self.mod_info.author,expand=True)
        self.description_tf = ft.TextField(label="描述", value=self.mod_info.description,multiline=True,expand=True)
        self.version_tf = ft.TextField(label="版本", value=self.mod_info.version,expand=True)
        print(self.mod_info.category)
        self.category_pk = TagPicker(selected_tags=self.mod_info.category)

        self.preview_imgs = ft.Row(
            wrap=True,
            spacing=10,
            run_spacing=10,
            scroll = ft.ScrollMode.AUTO,
        )

        self.meta_path = Path(self.mod_info.file_path).parent.parent / 'META'
        if not self.meta_path.exists():
            logger.warning(f"meta文件夹不存在，请检查路径：{self.meta_path}")
            return

        for img_path in self.meta_path.glob('*'):
            if judge_file_type(img_path) == FileType.IMAGE:
                self.preview_imgs.controls.append(
                    ft.Image(
                        src=str(img_path),
                    ))

        self.controls = [
            self.file_path_tf,
            self.name_tf,
            self.author_tf,
            self.version_tf,
            self.category_pk,
            self.description_tf,
            self.preview_imgs,
        ]

    def save_info(self):
        self.mod_info.name = self.name_tf.value
        self.mod_info.author = self.author_tf.value
        self.mod_info.description = self.description_tf.value
        self.mod_info.version = self.version_tf.value
        self.mod_info.category = self.category_pk.get_tags()

        with open(self.meta_path / 'info.json', 'w', encoding='utf-8') as f:
            json.dump(self.mod_info.model_dump(
                    by_alias=True,
                    exclude_none=True,
                    exclude={'file_path','file_name','file_stem'},
                    mode='json'),
                f, ensure_ascii=False, indent=4)

        self.update()
        pub.sendMessage(EventTopic.MOD_INFO_UPDATE.value, mod_path = self.mod_path, mod_info=self.mod_info)

@router.route('/detail')
class DetailView(ft.View):
    def build(self):
        self.mod_path : str = self.page.session.store.get('mod_path')
        self.detail_list = DetailList(self.mod_path)
        self.save_btn = ft.ElevatedButton(content="保存", on_click=self.save_info)
        self.controls = [
            NavBar(title="详情页"),
            self.save_btn,
            self.detail_list,
        ]

    def save_info(self, e):
        self.detail_list.save_info()
