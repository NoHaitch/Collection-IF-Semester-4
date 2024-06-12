import os
from src.item.Series import Series

import flet as ft
from flet import (
    Row,
    View,
    CupertinoAppBar,
    Container,
)

class EpisodeGUI:
    def __init__(self, back_button, cancel_button, page):
        self.back_button = back_button
        self.cancel_button = cancel_button
        self.episodeNumber = -1
        self.title = ""
        self.posterPath = os.path.abspath(os.path.join(
            os.path.dirname(__file__), '..', '..', 'db', 'poster', 'placeholder.png'))
        self.duration = 0
        self.episodeProgress = 0
        self.series = Series.listSeries[-1]
        self.numberOfEpisodes = 0

    def add_episode_view(self, page) -> View:
        self.numberOfEpisodes = int(str(page.route).removeprefix(f'/add_episode/'))
        return View(
            scroll=ft.ScrollMode.AUTO,
            route=page.route,
            controls=[
                CupertinoAppBar(
                    leading=self.back_button,
                ), self.add_episode_form()
            ],
            spacing=26
        )

    def add_episode_form(self):
        wrapper = Row(
            alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )

        allForms = []

        for i in range(self.numberOfEpisodes):
            tempform = ft.Column(
                [ft.TextField(label="Episode Number", hint_text="0"),
                ft.TextField(label="Title", hint_text="Episode n"),
                ft.TextField(label="Duration", hint_text="Duration in seconds"),
                ft.TextField(label="Episode Progress", hint_text="Progress in seconds"),
                ]
            )
            allForms.append(tempform)

        wrapper.controls.append(allForms)
        return Container(
            content=wrapper,
            padding=ft.Padding(top=20, left=20, right=20, bottom=20)
        )
        # submitButton = ft.ElevatedButton(
        #     text="Submit",
        #     onclick=lambda:
        # )