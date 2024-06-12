import flet as ft
from flet import (
    Row,
    TextButton,
    FilledButton,
    View,
    CupertinoAppBar,
    ElevatedButton,
    Icon,
)

from src.gui.content import Content


class Ongoing:
    def __init__(self, page, navigation: list[ElevatedButton],
                 quit_button: TextButton,
                 add_film_button: FilledButton,
                 add_series_button: FilledButton,
                 onclick_card_film,
                 onclick_card_series):
        # Create content
        self.content = Content(page, add_film_button, add_series_button, ft.colors.GREEN_ACCENT_400,
                               onclick_card_film, onclick_card_series)
        self.navigation = navigation
        self.quit_button = quit_button

    def ongoing_view(self) -> View:
        view = View(
            scroll=ft.ScrollMode.AUTO,
            route='/watchlist',
            controls=[
                CupertinoAppBar(
                    bgcolor=ft.colors.ORANGE_ACCENT_400,
                    leading=Icon(name=ft.icons.MOVIE_OUTLINED, color=ft.colors.BLACK),
                    trailing=self.quit_button,
                    middle=Row(
                        self.navigation,
                        alignment=ft.MainAxisAlignment.CENTER
                    ),

                ),
                self.content.create_content("Ongoing")
            ],
            spacing=26
        )

        return view
