import flet as ft
from config import settings
from loguru import logger
logger.add(sink= settings.log_dir + '/debug.log', enqueue=True, rotation='10 MB', level='DEBUG')


import views
from flet_router import router



def main(page: ft.Page):
    page.title = "自用 wad 管理器"
    page.scroll = ft.ScrollMode.AUTO
    def route_change():
        # if page.route.startswith(last_route):
        #     page.views.append(router.navigate(page.route))
        #     page.update()
        #     last_route = page.route
        #     return
        # print(f'切换到 {page.route}')
        new_view = router.navigate(page.route)
        if new_view in page.views:
            index = page.views.index(new_view)
            page.views = page.views[:index+1]
        else:
            page.views.append(new_view)
        # print(f'当前视图长度: {len(page.views)}')
        page.update()


    async def view_pop(e:ft.ViewPopEvent):
        # print(f'pop {e.view.route}')
        if e.view is not None:
            page.views.remove(e.view)
            top_view = page.views[-1]
            await page.push_route(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.views.clear()
    route_change()

if __name__ == "__main__":
    ft.run(main)