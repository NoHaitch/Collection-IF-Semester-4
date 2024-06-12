import flet as ft
from src.item.WatchItem import WatchItem
from flet import (
    Dropdown, Row, Container
)


class FilterGUI:

    def __init__(self):
        self.filter_list: str = "None"
        self.pagination_top = Row()
        self.cards: Container = Container()
        self.pagination_bot = Row()

    def filter_drop_down(self, status: str, pagination_top: Row, cards: Container, pagination_bot: Row, content) -> (
            Dropdown):
        self.pagination_top = pagination_top
        self.cards = cards
        self.pagination_bot = pagination_bot

        def on_genre_change(on_change_control: ft.ControlEvent):
            content.filter_list = on_change_control.control.value
            self.cards.content = Container()

            content.all_item, content.item_count = content.get_cards(status, content.sort_gui.sort_type,
                                                                     content.filter_list)

            if content.current_page * 24 > content.item_count:
                sub_items = content.all_item[(content.current_page - 1) * 24: content.item_count]
            else:
                sub_items = content.all_item[(content.current_page - 1) * 24: content.current_page * 24]

            temp: Container = content.create_cards(status, sub_items)
            temp.padding = 0
            self.cards.content = temp

            self.cards.update()

        dropdown = Dropdown(
            label="Filter By Genre",
            value="None",
            text_size=14,
            color=ft.colors.WHITE,
            width=120,
            item_height=30,

            label_style=ft.TextStyle(size=14, color=ft.colors.GREEN, weight=ft.FontWeight.BOLD),
            text_style=ft.TextStyle(size=14, color=ft.colors.GREEN, weight=ft.FontWeight.BOLD),
            options=[ft.dropdown.Option(genre) for genre in WatchItem.listGenre],
            on_change=on_genre_change
        )

        return dropdown
