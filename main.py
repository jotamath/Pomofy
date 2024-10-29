import flet as ft
from CardMemoria import memory_cards
from Pomodoro import pomodoro
from ToDo import todo

def main(page: ft.Page):
    def abrir_pomodoro(e):
        page.clean()
        pomodoro.main_pomodoro(page)

    def abrir_memory_cards(e):
        page.clean()
        memory_cards.main_memory_cards(page)

    def abrir_to_do(e):
        page.clean()
        todo.main_todo(page)

    pomodoro_button = ft.ElevatedButton(text="POMODORO", on_click=abrir_pomodoro)
    memory_cards_button = ft.ElevatedButton(text="MEMORY CARDS", on_click=abrir_memory_cards)
    to_do_button = ft.ElevatedButton(text="TO DO", on_click=abrir_to_do)

    page.add(ft.Column([
        pomodoro_button,
        memory_cards_button,
        to_do_button
    ]))

ft.app(target=main)
