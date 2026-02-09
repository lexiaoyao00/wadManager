import asyncio

import flet as ft
import views
from flet_router import router
from views.setting_view import DirViewWidget


def main(page: ft.Page):
    page.title = "自用 wad 管理器"
    page.scroll = ft.ScrollMode.AUTO
    def route_change():
        # if page.route.startswith(last_route):
        #     page.views.append(router.navigate(page.route))
        #     page.update()
        #     last_route = page.route
        #     return
        new_view = router.navigate(page.route)
        if new_view in page.views:
            index = page.views.index(new_view)
            page.views = page.views[:index+1]
        else:
            page.views.append(new_view)
        page.update()


    async def view_pop(e:ft.ViewPopEvent):
        if e.view is not None:
            page.views.remove(e.view)
            top_view = page.views[-1]
            await page.push_route(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.views.clear()
    route_change()

def test(page: ft.Page):
    tf = ft.TextField(label='test',
                         value='',
                         border=ft.InputBorder.OUTLINE,
                         text_size=20,
                         expand=1)
    btn = ft.IconButton(icon=ft.Icons.FOLDER_OPEN,tooltip='选择目录')
    path_row1 = ft.Row(expand=True,controls=[tf,btn])
    page.add(
        ft.Column(
            controls=[
                path_row1,
                ft.Row(expand=True,controls=[tf,btn]),
                DirViewWidget(name='test'),
            ]
        )
    )

if __name__ == "__main__":
    ft.run(main)