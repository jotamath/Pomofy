import flet as ft
import threading
import asyncio
from datetime import datetime, timedelta

class PomodoroTimer:
    def __init__(self):
        self.work_time = 25 * 60  # 25 minutos em segundos
        self.break_time = 5 * 60  # 5 minutos em segundos
        self.is_running = False
        self.time_left = self.work_time
        self.is_work_time = True

def main(page: ft.Page):
    page.title = "Pomodoro Timer"
    page.window_width = 400
    page.window_height = 600
    page.bgcolor = ft.colors.BLUE_GREY_900
    page.window_center()
    
    timer = PomodoroTimer()
    
    # Componentes visuais
    time_display = ft.Text(
        value="25:00",
        size=60,
        color=ft.colors.WHITE,
        weight=ft.FontWeight.BOLD,
        text_align=ft.TextAlign.CENTER,
    )
    
    status_text = ft.Text(
        value="Hora de Trabalhar!",
        size=20,
        color=ft.colors.WHITE,
        text_align=ft.TextAlign.CENTER,
    )
    
    progress_bar = ft.ProgressBar(
        width=300,
        color=ft.colors.GREEN_400,
        bgcolor=ft.colors.GREY_800,
        value=1.0
    )

    async def update_timer():
        while timer.is_running and timer.time_left >= 0:
            # Atualiza o display
            minutes = timer.time_left // 60
            seconds = timer.time_left % 60
            time_display.value = f"{minutes:02d}:{seconds:02d}"
            
            # Atualiza a barra de progresso
            total_time = timer.work_time if timer.is_work_time else timer.break_time
            progress = max(0, timer.time_left / total_time)
            progress_bar.value = progress
            
            page.update()
            
            # Espera 1 segundo
            await asyncio.sleep(1)
            
            if timer.time_left > 0:
                timer.time_left -= 1
            
            # Verifica se o timer chegou a zero
            if timer.time_left <= 0:
                if timer.is_work_time:
                    # Muda para o período de descanso
                    timer.is_work_time = False
                    timer.time_left = timer.break_time
                    status_text.value = "Hora do Descanso!"
                    progress_bar.color = ft.colors.BLUE_400
                else:
                    # Muda para o período de trabalho
                    timer.is_work_time = True
                    timer.time_left = timer.work_time
                    status_text.value = "Hora de Trabalhar!"
                    progress_bar.color = ft.colors.GREEN_400
                
                page.update()
    
    def start_asyncio_task(loop):
        asyncio.set_event_loop(loop)
        loop.run_until_complete(update_timer())

    def start_timer(e):
        if not timer.is_running:
            timer.is_running = True
            start_btn.visible = False
            pause_btn.visible = True
            reset_btn.visible = True
            page.update()
            
            # Inicia o timer em uma nova thread para evitar conflitos com o loop
            loop = asyncio.new_event_loop()
            threading.Thread(target=start_asyncio_task, args=(loop,)).start()
    
    def pause_timer(e):
        timer.is_running = False
        start_btn.visible = True
        pause_btn.visible = False
        page.update()
    
    def reset_timer(e):
        timer.is_running = False
        timer.is_work_time = True
        timer.time_left = timer.work_time
        status_text.value = "Hora de Trabalhar!"
        start_btn.visible = True
        pause_btn.visible = False
        progress_bar.color = ft.colors.GREEN_400
        progress_bar.value = 1.0
        
        minutes = timer.time_left // 60
        seconds = timer.time_left % 60
        time_display.value = f"{minutes:02d}:{seconds:02d}"
        
        page.update()
    
    # Botões
    start_btn = ft.ElevatedButton(
        "Iniciar",
        on_click=start_timer,
        style=ft.ButtonStyle(
            bgcolor=ft.colors.GREEN,
            color=ft.colors.WHITE,
            padding=20,
        ),
    )
    
    pause_btn = ft.ElevatedButton(
        "Pausar",
        on_click=pause_timer,
        visible=False,
        style=ft.ButtonStyle(
            bgcolor=ft.colors.ORANGE,
            color=ft.colors.WHITE,
            padding=20,
        ),
    )
    
    reset_btn = ft.ElevatedButton(
        "Reiniciar",
        on_click=reset_timer,
        style=ft.ButtonStyle(
            bgcolor=ft.colors.RED,
            color=ft.colors.WHITE,
            padding=20,
        ),
    )
    
    # Layout
    page.add(
        ft.Container(
            content=ft.Column(
                controls=[
                    ft.Container(height=50),
                    time_display,
                    ft.Container(height=10),
                    progress_bar,
                    ft.Container(height=20),
                    status_text,
                    ft.Container(height=30),
                    ft.Row(
                        controls=[start_btn, pause_btn, reset_btn],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            alignment=ft.alignment.center,
        )
    )

if __name__ == "__main__":
    ft.app(target=main)
