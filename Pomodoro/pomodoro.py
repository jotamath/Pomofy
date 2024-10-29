import flet as ft

def main_pomodoro(page: ft.Page):
    def voltar_menu_inicial(e):
        page.clean()
        main(page)

    page.add(ft.Text("Aplicação Pomodoro"))
    voltar_button = ft.ElevatedButton(text="Voltar ao Menu Inicial", on_click=voltar_menu_inicial)
    page.add(voltar_button)
