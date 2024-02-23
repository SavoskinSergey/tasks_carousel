import asyncio
from dotenv import load_dotenv
import os
import pprint
import random
import flet as ft
from app.utils.pomodoro import draw_pomodoro_view
from app.utils.pomodoro import Pomodoro
from app.task import Task
from carousel import Carousel
from database import add_task
from database import get_tasks

load_dotenv()
DEBUG = (os.getenv('DEBUG').lower() == 'true')


if DEBUG:
    v_data = [
        (
            'id' + str(i),
            'task' + str(i),
            'task_comment' + str(i),
            random.randint(1, 4)
        )
        for i in range(5)]
    v_data_from_bd = v_data
    print(v_data_from_bd, ' from bd')
else:
    v_data_from_bd = get_tasks()


class SliderPage():
    def __init__(self, name, comment, priority):
        self.context = ft.Column(
            [
                # ft.Text("Hello!", style=ft.TextThemeStyle.HEADLINE_MEDIUM),
                ft.Row(
                    [
                        # ft.Container(
                        #     expand=1
                        # ),
                        ft.Container(
                            ft.Text(
                                value=name,
                                theme_style=ft.TextThemeStyle.HEADLINE_MEDIUM,
                                size=42,
                                weight=ft.FontWeight.W_900,
                                italic=True,
                            ),
                            expand=11,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.START,
                ),
                ft.Row(
                    [
                        ft.Container(
                            expand=1,
                        ),
                        ft.Container(
                            expand=15,
                            content=ft.Text(
                                value=comment,
                                theme_style=ft.TextThemeStyle.HEADLINE_MEDIUM,
                                size=22,
                                italic=True,
                                color=ft.colors.BLUE_700,
                                max_lines=3
                            )
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.START,
                ),
                ft.Row(
                    [
                        ft.Container(
                            expand=7,
                        ),
                        ft.Container(
                            expand=1,
                            content=ft.Text(
                                value="p:" + str(priority),
                                theme_style=ft.TextThemeStyle.HEADLINE_MEDIUM,
                                size=22,
                                italic=True,
                                color=ft.colors.GREEN_400,
                            )
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.START,
                ),
            ],
            alignment=ft.alignment.center,
            height=200,
            # bgcolor=ft.colors.GREEN,
        )


class TodoApp(ft.UserControl):
    def __init__(self, page=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.page = page

    def build(self):
        print('------------------------run build------------------------------------')
        self.new_task_name_modal_field = ft.TextField(
            label="Name task",
            hint_text="What needs to be done?",
        )
        self.new_task_description_modal_field = ft.TextField(
            label="Description",
            multiline=True,
            min_lines=1,
            max_lines=5,
        )
        self.new_task_priority_modal_field = ft.Dropdown(
            label="Priority",
            width=200,
            options=[
                ft.dropdown.Option("1"),
                ft.dropdown.Option("2"),
                ft.dropdown.Option("3"),
                ft.dropdown.Option("4"),
            ],
        )
        self.add_task_modal = ft.AlertDialog(
            modal=True,
            title=ft.Text("Create new task:"),
            content=ft.Column(
                [
                    self.new_task_name_modal_field,
                    self.new_task_description_modal_field,
                    self.new_task_priority_modal_field,
                ],
                height=300,
                width=600,
            ),

            actions=[
                ft.TextButton("Add", on_click=self.add_task_create_modal),
                ft.TextButton("Cancel", on_click=self.close_task_create_modal),
            ],
            actions_alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            on_dismiss=lambda e: print("Modal dialog dismissed!"),
        )
        self.page.dialog = self.add_task_modal
        self.new_task_create_modal_button = ft.ElevatedButton(
            "+ Добавить задачу",
            right=True,
            on_click=self.show_task_create_modal_click
        )

        self.filter = ft.Tabs(
            scrollable=False,
            selected_index=0,
            on_change=self.tabs_changed,
            tabs=[
                ft.Tab(text="all"),
                ft.Tab(text="active"),
                ft.Tab(text="completed"),
                ft.Tab(text="detail")],
        )

        self.filter_important = ft.Tabs(
            scrollable=False,
            selected_index=0,
            # on_change=self.tabs_changed,
            tabs=[
                ft.Tab(text="Важные",),
                ft.Tab(text="Cрочные"),
                ft.Tab(text="Нужные"),
                ft.Tab(text="Прочие"),
            ],
        )
        self.slider_begin_page = ft.Column(
            [
                ft.Row(
                    [
                        ft.Container(
                            expand=1
                        ),
                        ft.Container(
                            ft.Text(
                                value="Hello!",
                                theme_style=ft.TextThemeStyle.HEADLINE_MEDIUM,
                                size=42,
                                weight=ft.FontWeight.W_900,
                                italic=True,
                            ),
                            expand=11,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.START,
                ),
                ft.Row(
                    [
                        ft.Container(
                            expand=1,
                        ),
                        ft.Container(
                            expand=7,
                            content=ft.Text(
                                value="123456789",
                                theme_style=ft.TextThemeStyle.HEADLINE_MEDIUM,
                                size=22,
                                italic=True,
                                color=ft.colors.BLUE_700,
                            )
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.START,
                ),
            ],
            alignment=ft.alignment.center,
            # width=200,
            height=200,
            # bgcolor=ft.colors.GREEN,
        )

        self.switcher = ft.AnimatedSwitcher(
            self.slider_begin_page,
            transition=ft.AnimatedSwitcherTransition.SCALE,
            duration=500,
            reverse_duration=100,
            switch_in_curve=ft.AnimationCurve.BOUNCE_OUT,
            switch_out_curve=ft.AnimationCurve.BOUNCE_IN,
        )

        self.switcher_block = ft.Row(
            [
                ft.Container(
                    content=ft.FloatingActionButton(
                        icon=ft.icons.NAVIGATE_BEFORE,
                        on_click=self.animate_prev,
                    ),
                    expand=1, height=200),
                ft.Column(
                    controls=[
                        self.switcher
                    ],
                    expand=10),
                ft.Container(
                    content=ft.FloatingActionButton(
                        # " ",
                        icon=ft.icons.NAVIGATE_NEXT,
                        on_click=self.animate_next,
                    ),
                    expand=1, height=200),
            ],
            height=200,
        )
        self.pomodoro = ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            width=200,
            controls=draw_pomodoro_view(self, "start_pomodoro"),
        )

        self.tasks = ft.Column()

        self.items_left = ft.Text("0 items left")
        self.cursor_tasks = 0

        return ft.Column(
            width=600,
            controls=[
                ft.Row(
                    [ft.Text(
                        value="Todos",
                        theme_style=ft.TextThemeStyle.HEADLINE_MEDIUM
                    )],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                ft.Row(
                    controls=[
                        self.new_task_create_modal_button,
                    ],
                ),
                ft.Column(
                    spacing=25,
                    controls=[
                        self.filter,
                        self.filter_important,
                        self.switcher_block,
                        self.pomodoro,
                        self.tasks,
                        ft.Row(
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            vertical_alignment=ft.CrossAxisAlignment.CENTER,
                            controls=[
                                self.items_left,
                                ft.OutlinedButton(
                                    text="Clear completed",
                                    on_click=self.clear_clicked
                                ),
                                ft.OutlinedButton(
                                    text="refresh_task",
                                    on_click=self.refresh_carousel
                                ),
                            ],
                        ),
                    ],
                ),

            ],
        )

    async def add_clicked(self, e):
        if self.new_task.value:
            task = Task(
                self.new_task.value,
                self.task_status_change,
                self.task_delete,
                comment=self.new_task_comment.value
            )
            self.tasks.controls.append(task)
            self.new_task.value = ""

            await self.new_task.focus_async()
            await self.update_async()

    async def add_task_create_modal(self, e):
        if self.new_task_name_modal_field.value:
            task_name = self.new_task_name_modal_field.value
            task_comment = self.new_task_description_modal_field.value
            task_priority = int(self.new_task_priority_modal_field.value)

            task = Task(
                task_name,
                self.task_status_change,
                self.task_delete,
                task_priority,
                task_comment
            )
            self.tasks.controls.append(task)
            task_item = ('id0000', task_name, task_comment, task_priority)
            self.page.carousel.items[task_priority].append(
                {'task': task_item, 'visible': 1, 'viewed': 0}
            )
            self.page.carousel.vision_count += 1
            pprint.pprint(self.page.carousel.items)

            add_task(task_name, task_comment, task_priority)
            self.new_task_name_modal_field.value = ""
            self.new_task_description_modal_field.value = ""
            self.new_task_priority_modal_field.value = ""

            await self.update_async()

        self.add_task_modal.open = False
        await self.page.update_async()

    async def close_task_create_modal(self, e):
        self.add_task_modal.open = False
        await self.page.update_async()

    async def show_task_create_modal_click(self, e):
        self.page.dialog = self.add_task_modal
        self.add_task_modal.open = True
        await self.page.update_async()

    async def task_status_change(self):
        await self.update_async()

    async def task_delete(self, task):
        self.tasks.controls.remove(task)
        await self.update_async()

    async def tabs_changed(self, e):
        await self.update_async()

    async def clear_clicked(self, e):
        for task in self.tasks.controls[:]:
            if task.completed:
                await self.task_delete(task)

    async def refresh_carousel(self, e):
        self.page.carousel.refresh()
        await self.animate_next(e)

    async def pomodoro_start(self, e):
        pomodoro_item = Pomodoro()
        self.current_pomodoro_item = pomodoro_item
        time_remainder = pomodoro_item.get_remainder(counter=0)
        self.pomodoro.controls = draw_pomodoro_view(
            self, time_remainder, refresh=True, pause=True, stop=True, start=False
        )
        await self.update_async()
        while pomodoro_item.time_remainder > -1 and self.current_pomodoro_item is pomodoro_item:
            await asyncio.sleep(1)
            time_remainder = pomodoro_item.get_remainder()
            self.pomodoro.controls[0] = ft.OutlinedButton(
                text=time_remainder,
                on_click=self.pomodoro_start
            )
            if self.current_pomodoro_item is pomodoro_item:
                await self.update_async()

    async def pomodoro_stop(self, e):
        self.current_pomodoro_item = Pomodoro()
        text_pomodoro = 'Start Pomodoro'
        self.pomodoro.controls = draw_pomodoro_view(
            self, text_pomodoro, start=True)

        await self.update_async()

    async def pomodoro_pause(self, e):
        self.current_pomodoro_item = Pomodoro(time_volume=self.current_pomodoro_item.time_remainder)
        time_remainder = self.current_pomodoro_item.get_remainder(counter=0)
        self.pomodoro.controls = draw_pomodoro_view(
            self, time_remainder, refresh=True, play=True, stop=True, start=False,
        )

        await self.update_async()

    async def pomodoro_play(self, e):
        pomodoro_item = self.current_pomodoro_item
        time_remainder = pomodoro_item.get_remainder(counter=0)
        self.pomodoro.controls = draw_pomodoro_view(
            self, time_remainder, refresh=True, pause=True, stop=True, start=False
        )
        await self.update_async()
        while pomodoro_item.time_remainder > -1 and self.current_pomodoro_item is pomodoro_item:
            await asyncio.sleep(1)
            time_remainder = pomodoro_item.get_remainder()
            self.pomodoro.controls[0] = ft.OutlinedButton(
                text=time_remainder,
                on_click=self.pomodoro_start
            )
            if self.current_pomodoro_item is pomodoro_item:
                await self.update_async()

    async def animate_next(self, e):
        task = self.page.carousel.get_slide()
        _, text, comment, priority = task['task']
        slider_page = SliderPage(text, comment, priority)
        self.switcher.content = slider_page.context

        await self.switcher.update_async()

    async def animate_prev(self, e):
        pass

    async def update_async(self):
        status = self.filter.tabs[self.filter.selected_index].text
        count = 0

        for task in self.tasks.controls:
            task.visible = (
                status == "all"
                or (status == "active" and task.completed is False)
                or (status == "completed" and task.completed)
            )
            if not task.completed:
                count += 1
        self.items_left.value = f"{count} active item(s) left"
        await super().update_async()


def connect_to_db():
    pass


def create_carousel():
    carousel = Carousel()
    for item in v_data_from_bd:
        if item:  # todo добавить проверку на актуальность
            carousel.items[item[3]].append({'task': item, 'visible': 1, 'viewed': 0})
            carousel.vision_count += 1
    return carousel


async def main(page: ft.Page):
    connect_to_db()
    page.carousel = create_carousel()
    page.title = "ToDo App"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.scroll = ft.ScrollMode.ADAPTIVE

    await page.add_async(
        TodoApp(page=page)
    )


ft.app(main)
