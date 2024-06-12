import os
import flet as ft
from flet import (
    Row,
    Text,
    Column,
    Container,
    Image,
    Icon,
    CupertinoButton
)

from src.item.WatchItem import WatchItem
from src.item.Film import Film
from src.item.Series import Series
from src.utils import Time


class Card:
    def __init__(self, page, onclick_card_film, onclick_card_series):
        self.current_page = 0
        self.page = page
        self.onclick_card_film = onclick_card_film
        self.onclick_card_series = onclick_card_series

    def create_card(self, watch_item: WatchItem, rating: bool = False, progress: bool = False):
        poster_path = os.path.abspath(
            os.path.join(
                os.path.dirname(__file__),
                '..',
                '..',
                'db',
                'poster',
                'placeholder.png')
        )

        img = Image(
            src=watch_item.posterPath,
            width=200,
            height=300
        )

        genre_list = watch_item.getGenre()
        genre_str = ""
        max_genre = 5

        if len(genre_list) < max_genre:
            max_genre = len(genre_list)

        for idx in range(0, max_genre):
            genre_str += genre_list[idx]
            if idx != max_genre - 1:
                genre_str += ", "

        card_content = Column(
            spacing=4,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            width=220,
            height=420,
        )

        # add image
        card_content.controls.append(img)

        # add texts
        card_text = Column(spacing=4,
                           alignment=ft.MainAxisAlignment.CENTER,
                           horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        card_text.controls.append(Text(watch_item.getTitle(),
                                       size=18,
                                       width=200,
                                       color=ft.colors.GREEN_ACCENT_400,
                                       weight=ft.FontWeight.BOLD,
                                       text_align=ft.TextAlign.CENTER))
        card_text.controls.append(Text(genre_str,
                                       size=12,
                                       width=200,
                                       color=ft.colors.GREY_700,
                                       text_align=ft.TextAlign.CENTER))
        card_content.controls.append(card_text)

        # add progress to card
        if progress:
            progress_row = Row(
                alignment=ft.MainAxisAlignment.CENTER,
                vertical_alignment=ft.CrossAxisAlignment.CENTER
            )

            # if film show duration progress
            if isinstance(watch_item, Film):
                film: Film | None = Film.cast_to_film(watch_item)
                progress_row.controls.append(Text(
                    "Time:",
                    size=12,
                    color=ft.colors.GREEN_600,
                    text_align=ft.TextAlign.CENTER,
                    weight=ft.FontWeight.BOLD,
                ))
                progress_row.controls.append(Text(
                    Time.seconds_to_hms(film.getProgress()),
                    size=12,
                    color=ft.colors.GREEN_600,
                    text_align=ft.TextAlign.CENTER,
                    weight=ft.FontWeight.BOLD,
                ))
                progress_row.controls.append(Text(
                    " / " + Time.seconds_to_hms(film.getDuration()),
                    size=12,
                    color=ft.colors.GREY_700,
                    text_align=ft.TextAlign.CENTER,
                    weight=ft.FontWeight.BOLD,
                ))

            else:  # if series shows episode progress
                series: Series | None = Series.cast_to_series(watch_item)
                progress_row.controls.append(Text(
                    "Episode:",
                    size=12,
                    color=ft.colors.GREEN_600,
                    text_align=ft.TextAlign.CENTER,
                    weight=ft.FontWeight.BOLD,
                ))
                progress_row.controls.append(Text(
                    series.getCurrentEpisode(),
                    size=12,
                    color=ft.colors.GREEN_600,
                    text_align=ft.TextAlign.CENTER,
                    weight=ft.FontWeight.BOLD,
                ))
                progress_row.controls.append(Text(
                    "/",
                    size=12,
                    color=ft.colors.GREY_700,
                    text_align=ft.TextAlign.CENTER,
                    weight=ft.FontWeight.BOLD,
                ))
                progress_row.controls.append(Text(
                    series.getTotalEpisode(),
                    size=12,
                    color=ft.colors.GREY_700,
                    text_align=ft.TextAlign.CENTER,
                    weight=ft.FontWeight.BOLD,
                ))
            progress_row.alignment = ft.MainAxisAlignment.CENTER
            card_content.controls.append(progress_row)

            # add last time watched
            last_watch_str = watch_item.getLastWatch().strftime('%d/%m/%Y')
            card_content.controls.append(Text(
                last_watch_str,
                size=12,
                color=ft.colors.GREY_700,
                text_align=ft.TextAlign.CENTER,
                weight=ft.FontWeight.BOLD
            ))

        # add rating and review
        if rating:
            rating_content = Column(
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            )

            # if not reviewed
            if watch_item.rating is None and watch_item.comments is None:
                rating_content.controls.append(Text(
                    "No review",
                    size=12,
                    color=ft.colors.GREY_700,
                    text_align=ft.TextAlign.CENTER,
                    weight=ft.FontWeight.BOLD
                ))

            else:  # item reviewed
                rating_row = Row(
                    alignment=ft.MainAxisAlignment.CENTER,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER
                )

                # add rating text
                if watch_item.getRating() is not None:
                    rating_text = Text(
                        round(watch_item.getRating(), 1),
                        size=14,
                        color=ft.colors.YELLOW_700,
                        text_align=ft.TextAlign.CENTER,
                        weight=ft.FontWeight.BOLD
                    )
                    rating_row.controls.append(rating_text)

                    # add rating star icon
                    rating_row.controls.append(
                        Column(
                            [Icon(
                                ft.icons.STAR,
                                size=14,
                                color=ft.colors.YELLOW_700,
                            )],
                            alignment=ft.MainAxisAlignment.CENTER,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER
                        )
                    )

                    rating_content.controls.append(rating_row)
                else:
                    rating_content.controls.append(Text(
                        "No Rating",
                        size=14,
                        color=ft.colors.YELLOW_700,
                        text_align=ft.TextAlign.CENTER,
                        weight=ft.FontWeight.BOLD
                    ))

                # add time of review
                last_watch_str = watch_item.getReviewDate().strftime('%d/%m/%Y')
                rating_content.controls.append(Text(
                    last_watch_str,
                    size=12,
                    color=ft.colors.GREY_700,
                    text_align=ft.TextAlign.CENTER,
                    weight=ft.FontWeight.BOLD
                ))

            card_content.controls.append(rating_content)

        if isinstance(watch_item, Film):
            return CupertinoButton(
                content=card_content,
                width=220,
                on_click=lambda _: self.onclick_card_film(self.page, watch_item.getID())
            )

        return CupertinoButton(
            content=card_content,
            width=220,
            on_click=lambda _: self.onclick_card_series(self.page, watch_item.getID())
        )

    def create_card_row(self, watch_item_list: list[WatchItem], rating: bool = False, progress: bool = False) -> Row:
        cards = [self.create_card(watch_item, rating, progress) for watch_item in watch_item_list]
        return Row(
            cards,
            tight=True,
            alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20
        )

    def create_card_col(self, watch_item_list: list[WatchItem],
                        rating: bool = False, progress: bool = False, card_per_row: int = 6):
        if len(watch_item_list) == 0:
            return Container(
                content=Column(
                    [
                        Text("No Item Found",
                             size=26,
                             weight=ft.FontWeight.BOLD,
                             color=ft.colors.GREEN_ACCENT_400),
                        Text("Add new item or change filter",
                             size=18,
                             color=ft.colors.GREEN_ACCENT_100)
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ), padding=ft.Padding(left=10, right=50, top=120, bottom=0)
            )

        col_list: list[Row] = []
        for i in range(0, (len(watch_item_list)//card_per_row)+1):
            col_list.append(
                self.create_card_row(watch_item_list[(i*card_per_row):(i*card_per_row)+card_per_row], rating, progress))
        return Column(
                    col_list,
                    scroll=ft.ScrollMode.ALWAYS,
                    alignment=ft.MainAxisAlignment.START,
                    horizontal_alignment=ft.CrossAxisAlignment.START,
                    spacing=24
            )
