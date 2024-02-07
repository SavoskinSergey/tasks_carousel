import flet as ft
import random


class Task(ft.UserControl):
    def __init__(
            self, task_name, task_status_change, task_delete, task_priority=0, comment=''
    ):
        super().__init__()
        self.completed = False
        self.task_name = task_name
        self.task_status_change = task_status_change
        self.task_priority = random.randint(1, 4)
        self.task_delete = task_delete
        self.task_comment = comment

    def build(self):
        self.display_task = ft.Checkbox(
            value=False, label=self.task_name[0:15], on_change=self.status_changed
        )
        self.edit_name = ft.TextField(label="Name Task",)
        self.edit_comment = ft.TextField(
            label="Description",
            multiline=True,
            min_lines=1,
            max_lines=5,
        )
        self.edit_priority = ft.Dropdown(
            label="Priority",
            width=200,
            options=[
                ft.dropdown.Option("1"),
                ft.dropdown.Option("2"),
                ft.dropdown.Option("3"),
                ft.dropdown.Option("4"),
            ],
        )

        self.display_view = ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                self.display_task,
                ft.Row(
                    spacing=0,
                    controls=[
                        ft.IconButton(
                            icon=ft.icons.DETAILS,
                            tooltip="Edit Details",
                            on_click=self.edit_clicked,
                        ),
                        ft.IconButton(
                            icon=ft.icons.CREATE_OUTLINED,
                            tooltip="Edit To-Do",
                            on_click=self.edit_clicked,
                        ),
                        ft.IconButton(
                            ft.icons.DELETE_OUTLINE,
                            tooltip="Delete To-Do",
                            on_click=self.delete_clicked,
                        ),
                    ],
                ),
            ],
        )

        self.edit_view = ft.Card(
            content=ft.Container(
                content=ft.Column(
                    [
                        # ft.Row(
                        #     [ft.Text(
                        #         "Name",
                        #     )]),
                        self.edit_name,
                        self.edit_comment,
                        self.edit_priority,
                        ft.Row(
                            [ft.TextButton(
                                "Save",
                                on_click=self.save_clicked
                            )],
                            alignment=ft.MainAxisAlignment.END,
                        ),
                    ]
                ),
                padding=10,
            ),
            visible=False,
        )

        return ft.Column(controls=[self.display_view, self.edit_view])

    async def edit_clicked(self, e):
        self.edit_name.value = self.task_name
        self.edit_comment.value = self.task_comment
        self.edit_priority.value = self.task_priority
        # self.edit_name.value = self.display_task.label
        self.display_view.visible = False
        self.edit_view.visible = True
        await self.update_async()

    async def save_clicked(self, e):
        self.task_name = self.edit_name.value
        self.task_comment = self.edit_comment.value
        self.task_priority = int((self.edit_priority.value if self.edit_priority.value else '4'))
        self.display_task.label = self.task_name[0:10]
        self.display_view.visible = True
        self.edit_view.visible = False
        await self.update_async()

    async def status_changed(self, e):
        self.completed = self.display_task.value
        await self.task_status_change(self)

    async def delete_clicked(self, e):
        await self.task_delete(self)
