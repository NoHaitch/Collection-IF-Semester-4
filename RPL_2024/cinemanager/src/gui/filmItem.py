import flet as ft
from flet import (
    View,
    CupertinoAppBar,
    Container,
    Row,
    Column,
    Text,
    ElevatedButton,
    Image,
    Icon,
    IconButton
)

from src.item.Film import Film
from src.utils import Time


class FilmItem:
    def __init__(self, page, back_button: IconButton, onclick_edit_film):
        self.back_button = back_button
        self.onclick_edit_film = onclick_edit_film
        self.page = page

    def film_item_view(self, film_id: int):
        film = Film.get_film_by_id(film_id)
        if film is None:
            self.page.go('/error')
            return

        self.page.title = "Film: " + film.title
        self.page.update()
        self.page.views.append(
            self.film_item_wrapper(film)
        )

    def film_item_wrapper(self, film):
        view = View(
            scroll=ft.ScrollMode.AUTO,
            route='/film/' + str(film.getID()),
            controls=[
                CupertinoAppBar(
                    leading=self.back_button,
                ), self.film_item_content(film)
            ],
            spacing=26
        )

        return view

    def film_item_content(self, film):
        wrapper = Container(
            alignment=ft.alignment.center,
        )

        content = Column(
            alignment=ft.MainAxisAlignment.CENTER
        )

        # add status
        status_col = Column(
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )

        status_col.controls.append(Text(
            "Status",
            size=14,
            color=ft.colors.GREY_700,
        ))

        status_text = Text(
            film.status,
            size=16,
            text_align=ft.TextAlign.CENTER,
            weight=ft.FontWeight.BOLD,
            color=ft.colors.WHITE,
        )
        if film.status == "Ongoing":
            status_text.color = ft.colors.ORANGE_ACCENT_400
        elif film.status == "Finished" or film.status == "Reviewed":
            status_text.color = ft.colors.PINK_ACCENT_400

        status_col.controls.append(Row(
            [status_text],
            width=1200,
            alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        ))
        content.controls.append(status_col)

        # add page title
        content.controls.append(Row(
            [Text(
                film.title,
                size=18,
                text_align=ft.TextAlign.CENTER,
                weight=ft.FontWeight.BOLD,
                color=ft.colors.GREEN_ACCENT_400
            )],
            width=1200,
            height=40,
            alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        ))

        # add image
        img = Image(
            src=film.posterPath,
            width=200,
            height=300
        )

        img_row = Row(
            [img],
            alignment=ft.MainAxisAlignment.CENTER,
            width=1200
        )
        content.controls.append(img_row)

        # add genre
        genre_str = ""
        for i in range(0, len(film.genre)):
            genre_str += film.genre[i]
            if i != len(film.genre) - 1:
                genre_str += ", "
        content.controls.append(Row(
            [Text(
                genre_str,
                color=ft.colors.GREY_500,
                width=400,
                text_align=ft.TextAlign.CENTER
            )],
            width=1200,
            alignment=ft.MainAxisAlignment.CENTER
        ))

        # add film progress and last watched
        if film.status == "Ongoing":
            progress_row = Row(
                alignment=ft.MainAxisAlignment.CENTER,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                width=1200
            )
            progress_row.controls.append(Text(
                "Time:",
                size=12,
                color=ft.colors.YELLOW_700,
                text_align=ft.TextAlign.CENTER,
                weight=ft.FontWeight.BOLD,
            ))
            progress_row.controls.append(Text(
                Time.seconds_to_hms(film.getProgress()),
                size=12,
                color=ft.colors.YELLOW_700,
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
            content.controls.append(progress_row)

        # add duration
        else:
            content.controls.append(Row(
                [Text(
                    "Duration: " + Time.seconds_to_hms(film.duration),
                    color=ft.colors.YELLOW_700,
                    width=200,
                    text_align=ft.TextAlign.CENTER
                )],
                width=1200,
                alignment=ft.MainAxisAlignment.CENTER
            ))

        # add rating and time reviewed
        if film.status == "Reviewed":
            rating_row = Row(
                width=1200,
                alignment=ft.MainAxisAlignment.CENTER,
                vertical_alignment=ft.CrossAxisAlignment.CENTER
            )

            # add rating text
            if film.rating is not None:
                rating_row.controls.append(Text(
                    round(film.getRating(), 2),
                    size=14,
                    color=ft.colors.YELLOW_700,
                    text_align=ft.TextAlign.CENTER,
                    weight=ft.FontWeight.BOLD
                ))
            else:
                rating_row.controls.append(Text(
                    "No Rating",
                    size=14,
                    color=ft.colors.YELLOW_700,
                    text_align=ft.TextAlign.CENTER,
                    weight=ft.FontWeight.BOLD
                ))

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

            content.controls.append(rating_row)

            # add comment
            if film.comments is not None:
                content.controls.append(
                    Row(
                        [Text(
                            film.comments,
                            size=12,
                            width=800,
                            color=ft.colors.PINK_ACCENT_400,
                            text_align=ft.TextAlign.CENTER,
                            weight=ft.FontWeight.BOLD
                        )],
                        width=1200,
                        alignment=ft.MainAxisAlignment.CENTER
                    )
                )

            # add time of review
            review_date = film.getReviewDate().strftime('%d/%m/%Y')
            content.controls.append(Text(
                "reviewed: " + review_date,
                size=12,
                width=1200,
                color=ft.colors.GREY_700,
                text_align=ft.TextAlign.CENTER,
                weight=ft.FontWeight.BOLD
            ))

        # add synopsis
        synopsis_col = Column(
            alignment=ft.MainAxisAlignment.CENTER
        )
        synopsis_row = Row(
            [Text(
                film.synopsis,
                color=ft.colors.GREEN_400,
                width=1000,
                text_align=ft.TextAlign.CENTER
            )],
            width=1200,
            alignment=ft.MainAxisAlignment.CENTER
        )
        synopsis_col.controls.append(Row([Text(
                "Synopsis",
                color=ft.colors.GREY_700,
                width=1200,
                text_align=ft.TextAlign.CENTER,
            )],
            height=50,
            width=1200,
            alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.CrossAxisAlignment.END
        ))
        synopsis_col.controls.append(synopsis_row)

        content.controls.append(synopsis_col)

        button_row = Row(
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=20,
            width=1200,
            height=50
        )

        # edit button
        edit_film_button = ElevatedButton(
            text="Edit Film and Progress",
            on_click=lambda _: self.onclick_edit_film(self.page, film.getID())
        )
        if film.status == "Unwatched":
            edit_film_button.text = "Edit Film and Add Progress"
        button_row.controls.append(edit_film_button)

        content.controls.append(button_row)

        wrapper.content = content

        return wrapper
