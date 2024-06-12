import flet as ft
from flet import (
    Dropdown,
    Row,
    Container
)


class SortGUI:

    def __init__(self):
        self.sort_type: str = "None"
        self.pagination_top = Row()
        self.cards: Container = Container()
        self.pagination_bot = Row()

    def sort_drop_down(self, status: str, pagination_top: Row, cards: Container, pagination_bot: Row,
                       content) -> Dropdown:
        self.pagination_top = pagination_top
        self.cards = cards
        self.pagination_bot = pagination_bot

        def on_dropdown_change(on_change_control: ft.ControlEvent):
            self.sort_type = on_change_control.control.value
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
            label="Sort By",
            value="Title",
            text_size=14,
            color=ft.colors.WHITE,
            width=200,
            item_height=30,

            label_style=ft.TextStyle(size=14, color=ft.colors.GREEN, weight=ft.FontWeight.BOLD),
            text_style=ft.TextStyle(size=14, color=ft.colors.GREEN, weight=ft.FontWeight.BOLD),
            options=[
                     ft.dropdown.Option("Title"),
                     ft.dropdown.Option("Rating"),
                     ft.dropdown.Option("Last Watch (Newest)"),
                     ft.dropdown.Option("Last Watch (Oldest)"),
                     ft.dropdown.Option("Review Date (Newest)"),
                     ft.dropdown.Option("Review Date (Oldest)"),
            ],
            on_change=on_dropdown_change
        )

        return dropdown
