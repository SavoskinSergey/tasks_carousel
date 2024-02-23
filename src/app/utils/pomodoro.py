from datetime import time
import flet as ft


class Pomodoro():
    id = 0

    def __init__(self, id=0, time_volume=180):
        if Pomodoro.id:
            self.id += 1
            Pomodoro.id += 1
        else:
            self.id = 1
            Pomodoro.id += 1
        self.time_remainder = time_volume

    def get_remainder(self, counter=1):
        self.time_remainder -= counter
        return time(0, self.time_remainder // 60, self.time_remainder % 60)


def draw_pomodoro_view(
        parent, text_content: str = '',
        refresh: bool = False,
        pause: bool = False,
        stop: bool = False,
        play: bool = False,
        start: bool = True) -> list:

    pomodoro_context = []
    pomodoro_context.append(
        ft.OutlinedButton(
            text=text_content,
            on_click=parent.pomodoro_start
        )
    )
    if refresh:
        pomodoro_context.append(
            ft.IconButton(
                icon=ft.icons.REFRESH,
                tooltip="Start Again",
                on_click=parent.pomodoro_start,
            )
        )
    if pause:
        pomodoro_context.append(
            ft.IconButton(
                icon=ft.icons.PAUSE,
                tooltip="Pause",
                on_click=parent.pomodoro_pause,
            )
        )
    if play:
        pomodoro_context.append(
            ft.IconButton(
                icon=ft.icons.PLAY_ARROW,
                tooltip="Play",
                on_click=parent.pomodoro_play,
            )
        )

    if start:
        pomodoro_context.append(
            ft.IconButton(
                icon=ft.icons.PLAY_ARROW,
                tooltip="Start Timer",
                on_click=parent.pomodoro_start,
            )
        )

    if stop:
        pomodoro_context.append(
            ft.IconButton(
                icon=ft.icons.STOP,
                tooltip="Stop pomodoro",
                on_click=parent.pomodoro_stop,
            )
        )
    return pomodoro_context
