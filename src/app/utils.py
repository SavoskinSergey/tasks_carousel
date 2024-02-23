import flet as ft


def draw_pomodoro_view(
        parent, text_content: str = '',
        refresh: bool = False,
        pause: bool = False,
        stop: bool = False,
        play: bool = False,
        start: bool = True) -> list:
    """Конструктор панельки помодоро
    можно накидывать кнопки параметрами. """

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
