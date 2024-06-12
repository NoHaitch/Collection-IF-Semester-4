import flet as ft
from flet import (
    Page,
    Text,
    View,
    Icon,
    CrossAxisAlignment,
    MainAxisAlignment,
    IconButton,
    ElevatedButton,
    TextButton,
    FilledButton
)

from src.gui.watchlist import Watchlist
from src.gui.ongoing import Ongoing
from src.gui.finished import Finished
from src.gui.filmGUI import FilmGUI
from src.gui.seriesGUI import SeriesGUI
from src.gui.episodeGUI import EpisodeGUI
from src.gui.filmItem import FilmItem
from src.gui.seriesItem import SeriesItem
from src.gui.filmEdit import FilmEdit
from src.gui.seriesEdit import SeriesEdit
from src.item.Film import Film
from src.item.Series import Series


class GUI:
    """
    Create and manage GUI
    """
    def __init__(self):
        self.history = []  # stack

    def main_page(self, page: Page) -> None:
        page.title = "Cinemanager Watchlist"
        page.theme_mode = ft.ThemeMode.DARK
        page.vertical_alignment = ft.MainAxisAlignment.CENTER
        page.horizontal_alignment = ft.MainAxisAlignment.CENTER
        page.window_resizable = False
        page.window_center()

        # onclick functions
        def onclick_watchlist(page_ptr: Page):
            page_ptr.go('/watchlist')
            self.history.append('/watchlist')
            if len(self.history) > 5:
                self.history.pop(0)

        def onclick_ongoing(page_ptr: Page):
            page_ptr.go('/ongoing')
            self.history.append('/ongoing')
            if len(self.history) > 5:
                self.history.pop(0)

        def onclick_finished(page_ptr: Page):
            page_ptr.go('/finished')
            self.history.append('/finished')
            if len(self.history) > 5:
                self.history.pop(0)

        def onclick_add_film(page_ptr: Page):
            page_ptr.go('/add_film')

        def onclick_add_series(page_ptr: Page):
            page_ptr.go('/add_series')

        def onclick_back(page_ptr):
            if len(self.history) > 0:
                page_ptr.go(self.history[-1])
                self.history.pop()
            else:
                page_ptr.go('/watchlist')

        def onclick_card_film(page_ptr, id_film):
            page_ptr.go('/film/' + str(id_film))

        def onclick_card_series(page_ptr, id_series):
            page_ptr.go('/series/' + str(id_series))

        def onclick_edit_film(page_ptr, id_film):
            page_ptr.go('/edit_film/' + str(id_film))

        def onclick_edit_series(page_ptr, id_series):
            page_ptr.go('/edit_series/' + str(id_series))

        # Navigation Buttons
        navigation: list[ElevatedButton] = [ElevatedButton(
            text="Watchlist",
            on_click=lambda _: onclick_watchlist(page),
            color=ft.colors.WHITE,
            height=30
        ), ElevatedButton(
            text="Ongoing",
            on_click=lambda _: onclick_ongoing(page),
            color=ft.colors.WHITE,
            height=30
        ), ElevatedButton(
            text="Finished",
            on_click=lambda _: onclick_finished(page),
            color=ft.colors.WHITE,
            height=30
        )]

        quit_button = TextButton(
            content=Text("Quit", color=ft.colors.BLACK),
            on_click=lambda _: page.window_close(),
        )

        back_button = IconButton(
            icon=ft.icons.ARROW_BACK_ROUNDED,
            icon_size=32,
            icon_color=ft.colors.GREEN_ACCENT_400,
            on_click=lambda _: onclick_back(page),
        )

        cancel_button = TextButton(
            text="Cancel",
            on_click=lambda _: onclick_back(page),
        )

        add_film_button = FilledButton(
            content=Text("Add Film", size=12,
                         text_align=ft.TextAlign.CENTER),
            width=128,
            height=24,
            on_click=lambda _: onclick_add_film(page)
        )

        add_series_button = FilledButton(
            content=Text("Add Series", size=12,
                         text_align=ft.TextAlign.CENTER),
            width=128,
            height=24,
            on_click=lambda _: onclick_add_series(page)
        )

        watchlist = Watchlist(page, navigation, quit_button, add_film_button, add_series_button,
                              onclick_card_film, onclick_card_series)
        ongoing = Ongoing(page, navigation, quit_button, add_film_button, add_series_button,
                          onclick_card_film, onclick_card_series)
        finished = Finished(page, navigation, quit_button, add_film_button, add_series_button,
                            onclick_card_film, onclick_card_series)
        film_gui = FilmGUI(back_button, cancel_button)
        series_gui = SeriesGUI(back_button, cancel_button, page)
        episode_gui = EpisodeGUI(back_button, cancel_button, page)
        film_item = FilmItem(page, back_button, onclick_edit_film)
        series_item = SeriesItem(page, back_button, onclick_edit_series)
        film_edit = FilmEdit(page, back_button, cancel_button)
        series_edit = SeriesEdit(page, back_button, cancel_button)

        print("Starting route:", page.route)

        def route_change(e):
            """
            page router\n
            - Home : "/"\n
            - Watchlist : "/watchlist\n
            - Ongoing : "/ongoing"\n
            - Finished : "/finished"\n
            - add film: "/add_film"\n
            - add series: "/add_series"\n
            - add episode: "/add_episode"\n
            - film item page: "./film/item_id"\n
            - series item page: "./series/item_id"\n
            """
            print("Route change:", e.route)
            page.views.clear()

            # Home Page
            if page.route == '/':
                page.window_center()
                page.window_height = 500
                page.window_width = 500
                page.views.append(
                    View(
                        route='/',
                        vertical_alignment=MainAxisAlignment.CENTER,
                        horizontal_alignment=CrossAxisAlignment.CENTER,
                        controls=[
                            Icon(ft.icons.MOVIE_OUTLINED, size=128),
                            Text("Cinemanager",
                                 text_align=ft.TextAlign.CENTER,
                                 size=32,
                                 weight=ft.FontWeight.BOLD),
                            ElevatedButton(text='Watchlist', on_click=lambda _: page.go('/watchlist'))
                        ],
                        spacing=26
                    )
                )

            # Watchlist
            if page.route == '/watchlist':
                page.title = "Cinemanager Watchlist"
                page.window_width = 1600
                page.window_height = 900
                page.window_center()

                # add view to page
                page.views.append(
                    watchlist.watchlist_view()
                )

            # Ongoing
            if page.route == '/ongoing':
                page.title = "Cinemanager Ongoing"
                page.window_width = 1600
                page.window_height = 900
                page.window_center()

                # add view to page
                page.views.append(
                    ongoing.ongoing_view()
                )

            # Finished
            if page.route == '/finished':
                page.title = "Cinemanager Finished"
                page.window_width = 1600
                page.window_height = 900
                page.window_center()

                # add view to page
                page.views.append(
                    finished.finished_view()
                )

            # add film
            if page.route == '/add_film':
                page.title = "Cinemanager Add a New Film"
                page.window_width = 1600
                page.window_height = 900
                page.window_center()

                # add view to page
                page.views.append(
                    film_gui.add_film_view()
                )

            # add series
            if page.route == '/add_series':
                page.title = "Cinemanager Add a New Series"
                page.window_width = 1600
                page.window_height = 900
                page.window_center()

                # add view to page
                page.views.append(
                    series_gui.add_series_view()
                )

            # add episode
            if '/add_episode/' in page.route:
                page.title = "Cinemanager Add a New Episode"
                page.window_width = 1600
                page.window_height = 900
                page.window_center()

                # add view to page
                page.views.append(
                    episode_gui.add_episode_view(page)
                )


            if '/film/' in page.route:
                film_id = int(str(page.route).removeprefix('/film/'))

                page.window_width = 1600
                page.window_height = 900
                page.window_center()

                film = Film.get_film_by_id(film_id)
                if film is None:
                    page.go('/error')
                    return

                page.title = "Film: " + film.title
                page.views.append(
                    film_item.film_item_wrapper(film)
                )

            if '/series/' in page.route:
                series_id = int(str(page.route).removeprefix('/series/'))

                page.window_width = 1600
                page.window_height = 900
                page.window_center()

                series = Series.get_series_by_id(series_id)
                if series is None:
                    page.go('/error')
                    return

                page.title = "Series: " + series.title
                page.views.append(
                    series_item.series_item_wrapper(series)
                )

            if '/edit_film' in page.route:
                film_id = int(str(page.route).removeprefix('/edit_film/'))

                page.window_width = 1600
                page.window_height = 900
                page.window_center()

                film = Film.get_film_by_id(film_id)
                if film is None:
                    page.go('/error')
                    return

                page.title = "Editing Film: " + film.title
                page.views.append(
                    film_edit.film_edit_wrapper(film)
                )

            if '/edit_series' in page.route:
                series_id = int(str(page.route).removeprefix('/edit_series/'))

                page.window_width = 1600
                page.window_height = 900
                page.window_center()

                series = Series.get_series_by_id(series_id)
                if series is None:
                    page.go('/error')
                    return

                page.title = "Editing Series: " + series.title
                page.views.append(
                    series_edit.series_edit_wrapper(series)
                )

            page.update()

        def view_pop(e):
            print("View pop:", e.view)
            page.views.pop()
            top_view = page.views[-1]
            page.go(top_view.route)

        page.on_route_change = route_change
        page.on_view_pop = view_pop
        page.go(page.route)
