import math

import flet as ft
from flet import (
    Container,
    Column,
    FilledButton,
    Row,
    Text,
    ElevatedButton
)

from src.item.WatchItem import WatchItem
from src.item.Film import Film
from src.item.Series import Series
from src.gui.filterGUI import FilterGUI
from src.gui.sortGUI import SortGUI
from src.gui.card import Card


class Content:
    def __init__(self, page, add_film_button: FilledButton, add_series_button: FilledButton, theme_color: str,
                 onclick_card_film, onclick_card_series):
        self.page = page
        self.card = Card(page, onclick_card_film, onclick_card_series)
        self.sort_gui = SortGUI()
        self.filter_gui = FilterGUI()
        self.current_page = 1
        self.filter_dropdown = None
        self.sort_dropdown = None
        self.item_count = 0
        self.status = None
        self.add_film_button = add_film_button
        self.add_series_button = add_series_button
        self.theme_color = theme_color
        self.sort_value = None
        self.filter_list = None
        self.all_item = None

    @staticmethod
    def item_count_text(item_count) -> Text:
        return Text(
            "Jumlah Item: " + str(item_count),
            size=14,
            weight=ft.FontWeight.BOLD
        )

    def create_content(self, status: str) -> Container:
        self.status = status

        content = Container(
            padding=ft.padding.only(50, 0, 50, 0)
        )

        self.all_item, self.item_count = self.get_cards(status, self.sort_gui.sort_type, self.filter_list)
        print("line 55 content : ", self.sort_gui.sort_type)

        total_page = math.ceil(self.item_count/24)

        content_column = Column(
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )

        pagination_top = self.create_pagination_buttons(self.current_page, total_page, content_column, self.all_item)

        if self.current_page * 24 > self.item_count:
            sub_items = self.all_item[(self.current_page - 1) * 24: self.item_count]
        else:
            sub_items = self.all_item[(self.current_page - 1) * 24: self.current_page * 24]

        cards = self.create_cards(self.status, sub_items)

        pagination_bot = Row()
        if len(sub_items) > 6:
            pagination_bot = self.create_pagination_buttons(self.current_page, total_page, content_column,
                                                            self.all_item)

        self.filter_dropdown = self.filter_gui.filter_drop_down(status, pagination_top, cards, pagination_bot, self)
        self.sort_dropdown = self.sort_gui.sort_drop_down(status, pagination_top, cards, pagination_bot, self)
        content_column.controls.append(
            Row([
                Row([
                    self.filter_dropdown,
                    self.sort_dropdown]),
                Row([
                    Content.item_count_text(self.item_count),
                    Column([self.add_film_button,
                            self.add_series_button],
                           alignment=ft.MainAxisAlignment.CENTER,
                           )
                ], spacing=40)
            ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            )
        )

        content_column.controls.append(pagination_top)
        content_column.controls.append(cards)
        content_column.controls.append(pagination_bot)
        content.content = content_column
        return content

    def get_cards(self, status: str, sort_type: str | None = None, filter_list: str | list[str] = None, ) \
            -> tuple[list[WatchItem], int]:

        content_items: list[WatchItem] = []
        for film in Film.listFilm:
            content_items.append(film)
        for series in Series.listSeries:
            content_items.append(series)
        content_items = WatchItem.sortByAlphabet(content_items, isAscending=True)

        content_items = WatchItem.filterByStatus(content_items, status)

        if filter_list is not None:
            content_items = WatchItem.filterByGenre(content_items, filter_list)

        if sort_type is not None and sort_type != "Title":  # Rating, Last Watch, Review Date
            if sort_type == "Rating":
                content_items = WatchItem.sortByRating(content_items)
            elif sort_type == "Last Watch (Newest)":
                content_items = WatchItem.sortByLastWatchedNewest(content_items)
            elif sort_type == "Last Watch (Oldest)":
                content_items = WatchItem.sortByLastWatchedOldest(content_items)
            elif sort_type == "Review Date (Newest)":
                content_items = WatchItem.sortByReviewDateNewest(content_items)
            elif sort_type == "Review Date (Oldest)":
                content_items = WatchItem.sortByReviewDateOldest(content_items)
            # for item in content_items:
                # print(str(item.getReviewDate()) + " " + item.getTitle())

        return content_items, len(content_items)

    def create_pagination_buttons(self, current_page: int, total_page: int,
                                  content_column, all_item) -> Row:
        pagination_row = Row(
            alignment=ft.MainAxisAlignment.CENTER
        )

        if total_page < 2:
            return pagination_row

        def change_page(_, new_page: int):
            self.current_page = new_page
            content_column.controls.clear()

            pagination_top = self.create_pagination_buttons(new_page, total_page, content_column, self.all_item)

            if self.current_page * 24 > self.item_count:
                sub_items = self.all_item[(self.current_page - 1) * 24: self.item_count]
            else:
                sub_items = self.all_item[(self.current_page - 1) * 24: self.current_page * 24]

            cards = self.create_cards(self.status, sub_items)

            pagination_bot = Row()
            if len(sub_items) > 6:
                pagination_bot = self.create_pagination_buttons(new_page, total_page, content_column, all_item)

            content_column.controls.append(
                Row([
                    Row([
                        self.filter_dropdown,
                        self.sort_dropdown]),
                    Row([
                        Content.item_count_text(self.item_count),
                        Column([self.add_film_button,
                                self.add_series_button],
                               alignment=ft.MainAxisAlignment.CENTER,
                               )
                    ], spacing=40)
                ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                )
            )

            content_column.controls.append(pagination_top)
            content_column.controls.append(cards)
            content_column.controls.append(pagination_bot)

            content_column.update()

        # link to first page
        pagination_row.controls.append(
            ElevatedButton(
                content=Text("start", size=12, color=ft.colors.BLACK),
                bgcolor=ft.colors.BLUE_GREY_700,
                on_click=lambda e: change_page(e, 1)
            )
        )

        if current_page < 4:
            for i in range(1, total_page + 1):
                if i == current_page:
                    pagination_row.controls.append(
                        ElevatedButton(
                            content=Text(str(i), size=14, color=ft.colors.BLACK),
                            bgcolor=ft.colors.BLUE_GREY_700,
                            on_click=lambda e, new_page=i: change_page(e, new_page)
                        )
                    )
                else:
                    pagination_row.controls.append(
                        ElevatedButton(
                            content=Text(str(i), size=14, color=ft.colors.BLACK),
                            bgcolor=self.theme_color,
                            on_click=lambda e, new_page=i: change_page(e, new_page)
                        )
                    )

                if i == 5:
                    break
        elif current_page > total_page - 2:
            for i in range(total_page-4, total_page + 1):
                if i == current_page:
                    pagination_row.controls.append(
                        ElevatedButton(
                            content=Text(str(i), size=14, color=ft.colors.BLACK),
                            bgcolor=ft.colors.BLUE_GREY_700,
                            on_click=lambda e, new_page=i: change_page(e, new_page)
                        )
                    )
                else:
                    pagination_row.controls.append(
                        ElevatedButton(
                            content=Text(str(i), size=14, color=ft.colors.BLACK),
                            bgcolor=self.theme_color,
                            on_click=lambda e, new_page=i: change_page(e, new_page)
                        )
                    )
        else:
            for i in range(current_page-2, current_page+3):
                if i == current_page:
                    pagination_row.controls.append(
                        ElevatedButton(
                            content=Text(str(i), size=14, color=ft.colors.BLACK),
                            bgcolor=ft.colors.BLUE_GREY_700,
                            on_click=lambda e, new_page=i: change_page(e, new_page)
                        )
                    )
                else:
                    pagination_row.controls.append(
                        ElevatedButton(
                            content=Text(str(i), size=14, color=ft.colors.BLACK),
                            bgcolor=self.theme_color,
                            on_click=lambda e, new_page=i: change_page(e, new_page)
                        )
                    )

        # link to last page
        pagination_row.controls.append(
            ElevatedButton(
                content=Text("last", size=12, color=ft.colors.BLACK),
                bgcolor=ft.colors.BLUE_GREY_700,
                on_click=lambda e: change_page(e, total_page)
            )
        )

        return pagination_row

    def create_cards(self, status: str, items_list: list[WatchItem]):
        rating = False
        progress = False
        if status == "Ongoing":
            progress = True
        elif status == "Finished" or status == "Reviewed":
            rating = True

        return Container(
            content=self.card.create_card_col(items_list, rating, progress),
            padding=20
        )
