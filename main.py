import flet as ft
from widgets.mod_label import ModLabel
from schemas.mod_info import ModInfo
from views.setting_view import SettingView
from config import settings,save_settings,BaseSettings

def main(page: ft.Page):
    page.scroll = ft.ScrollMode.AUTO


    gird_layout = ft.Row(
        wrap=True,
        spacing=10,
        run_spacing=10,
        controls=[
            ModLabel(ModInfo(file_path="assets/img/10658727.jpg",cover="assets/img/10658727.jpg")),
            ModLabel(ModInfo(file_path="assets/img/10688417.jpg",cover="assets/img/10688417.jpg")),
            ModLabel(ModInfo(file_path="assets/img/10679892.jpg",cover="assets/img/10679892.jpg")),
            ModLabel(ModInfo(file_path="assets/img/10695071.jpg",cover="assets/img/10695071.jpg")),
            ModLabel(ModInfo(file_path="assets/img/10710725.jpg",cover="assets/img/10710725.jpg")),
            ModLabel(ModInfo(file_path="assets/img/10664862.jpg",cover="assets/img/10664862.jpg")),
            ModLabel(ModInfo(file_path="assets/img/10683420.jpg",cover="assets/img/10683420.jpg")),
            ModLabel(ModInfo(file_path="assets/img/10713902.png",cover="assets/img/10713902.png")),
        ]
    )
    page.add(gird_layout)

    # setting_page = SettingView()

    # page.add(setting_page)



if __name__ == "__main__":
    ft.run(main)