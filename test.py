import flet as ft
from views.detail_view import TagPicker

def main(page: ft.Page):
    page.title = "自动补全标签输入示例"
    tag_picker = TagPicker()
    page.add(tag_picker)

ft.run(main)
