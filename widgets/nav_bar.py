import flet as ft
import asyncio


@ft.control
class NavBar(ft.AppBar):
    def build(self):
        self.actions = [
            ft.IconButton(icon=ft.Icons.HOME, on_click = lambda: asyncio.create_task(self.page.push_route("/"))),
            ft.IconButton(icon=ft.Icons.SETTINGS, on_click = lambda: asyncio.create_task(self.page.push_route("/settings"))),
        ]