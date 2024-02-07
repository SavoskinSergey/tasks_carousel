import flet as ft
from app.task import Task

# import psycopg2

# try:
#     conn = psycopg2.connect(
#         dbname="flet", user="saleor", password="123", host="127.0.0.1"
#     )
#     cursor = conn.cursor()
#     print('connection to pg')
#     cursor.execute(
#         'INSERT INTO tasks (name, comment, priority) VALUES (%s, %s, %s)',
#         ('first', 'comment2', 5)
#     )
#     cursor.execute("SELECT * FROM tasks;")
#     # print(cursor.fetchall())
#     conn.commit()

# except Exception as e:
#     # в случае сбоя подключения будет выведено сообщение  в STDOUT
#     print(e)
#     print('Can`t establish connection to database')

# cursor.close()  # закрываем курсор
# conn.close()    # закрываем подключение


class SliderPage():
    def __init__(self, name, comment, priority):
        self.context = ft.Column(
            [
                # ft.Text("Hello!", style=ft.TextThemeStyle.HEADLINE_MEDIUM),
                ft.Row(
                    [
                        ft.Container(
                            expand=1
                        ),
                        ft.Container(
                            ft.Text(
                                value=name, style=ft.TextThemeStyle.HEADLINE_MEDIUM,
                                size=48,
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
                                value=comment,
                                style=ft.TextThemeStyle.HEADLINE_MEDIUM,
                                size=28,
                                italic=True,
                                color=ft.colors.BLUE_300,
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
                                value=", pr - " + str(priority),
                                style=ft.TextThemeStyle.HEADLINE_MEDIUM,
                                size=28,
                                italic=True,
                                color=ft.colors.BLUE_300,
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
        # self.new_task = ft.TextField(
        #     hint_text="What needs to be done?",
        #     on_submit=self.add_clicked,
        #     expand=True
        # )

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
                                value="Hello!", style=ft.TextThemeStyle.HEADLINE_MEDIUM,
                                size=48,
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
                                value="123456789", style=ft.TextThemeStyle.HEADLINE_MEDIUM,
                                size=28,
                                italic=True,
                                color=ft.colors.BLUE_300,
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

        self.tasks = ft.Column()

        self.items_left = ft.Text("0 items left")
        self.cursor_tasks = 0

        return ft.Column(
            width=600,
            controls=[
                ft.Row(
                    [ft.Text(
                        value="Todos", style=ft.TextThemeStyle.HEADLINE_MEDIUM
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
            task = Task(
                self.new_task_name_modal_field.value,
                self.task_status_change,
                self.task_delete,
                comment=self.new_task_description_modal_field.value
            )
            self.tasks.controls.append(task)

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

    async def animate_next(self, e):
        if self.cursor_tasks < len(self.tasks.controls) - 1:
            self.cursor_tasks += 1
        else:
            self.cursor_tasks = 0
        text = self.tasks.controls[self.cursor_tasks].task_name
        comment = self.tasks.controls[self.cursor_tasks].task_comment
        priority = self.tasks.controls[self.cursor_tasks].task_priority
        slider_page = SliderPage(text, comment, priority)
        self.switcher.content = slider_page.context
        await self.switcher.update_async()

    async def animate_prev(self, e):
        if self.cursor_tasks < 1:
            self.cursor_tasks = len(self.tasks.controls) - 1
        else:
            self.cursor_tasks -= 1
        text = self.tasks.controls[self.cursor_tasks].task_name
        comment = self.tasks.controls[self.cursor_tasks].task_comment
        priority = self.tasks.controls[self.cursor_tasks].task_priority
        slider_page = SliderPage(text, comment, priority)

        self.switcher.content = slider_page.context
        await self.switcher.update_async()

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


async def main(page: ft.Page):
    page.title = "ToDo App"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.scroll = ft.ScrollMode.ADAPTIVE

    await page.add_async(
        TodoApp(page=page)
    )


ft.app(main)
