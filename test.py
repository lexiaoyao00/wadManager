import flet as ft


@ft.control
class Task(ft.Row):
    text: str = ""
    txt_expand : int = 0

    def init(self):
        self.text_edit = ft.TextField(value=self.text, expand= self.txt_expand)
        self.edit_button = ft.IconButton(icon=ft.Icons.EDIT)
        self.controls = [self.text_edit, self.edit_button]


def main(page: ft.Page):
    page.add(
        Task(text="Do laundry"),
        Task(text="Cook dinner",txt_expand = 1),
        ft.Row(controls=[
            ft.TextField(value="sleep", expand= 1),
            ft.IconButton(icon=ft.Icons.EDIT)
            ])
    )


ft.run(main)