import flet as ft
from flet import(
    View,
    CupertinoAppBar,
    Container,
    Row,
    Column,
    Text,
    ElevatedButton,
    Image,
    Icon,
    IconButton,
    DataTable
)

from src.item.Series import Series
from src.utils import Time

class SeriesItem:
    def __init__(self, page, back_button: IconButton, onclick_edit_series):
        self.back_button = back_button
        self.onclick_edit_series = onclick_edit_series
        self.page = page

    def series_item_view(self, series_id: int):
        series = Series.get_series_by_id(series_id)
        if series is None:
            self.page.go('/error')
            return

        self.page.title = "Series: " + series.title
        self.page.views.append(
            self.series_item_wrapper(series)
        )

    def series_item_wrapper(self, series):
        view = View(
            scroll=ft.ScrollMode.AUTO,
            route='/series/' + str(series.getID()),
            controls=[
                CupertinoAppBar(
                    leading=self.back_button,
                ), self.series_item_content(series)
            ],
            spacing=26
        )

        return view

    def series_item_content(self, series):
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
            series.status,
            size=16,
            text_align=ft.TextAlign.CENTER,
            weight=ft.FontWeight.BOLD,
            color=ft.colors.WHITE,
        )
        if series.status == "Ongoing":
            status_text.color = ft.colors.ORANGE_ACCENT_400
        elif series.status == "Finished" or series.status == "Reviewed":
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
                series.title,
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
            src=series.posterPath,
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
        for i in range(0, len(series.genre)):
            genre_str += series.genre[i]
            if i != len(series.genre) - 1:
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

        # add series current and total episode
        if series.status == "Ongoing":
            progress_row = Row(
                alignment=ft.MainAxisAlignment.CENTER,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                width=1200
            )
            progress_row.controls.append(Text(
                "Episode:",
                size=12,
                color=ft.colors.YELLOW_700,
                text_align=ft.TextAlign.CENTER,
                weight=ft.FontWeight.BOLD,
            ))
            progress_row.controls.append(Text(
                series.getCurrentEpisode(),
                size=12,
                color=ft.colors.YELLOW_700,
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
            content.controls.append(progress_row)

        # add total episode
        else:
            content.controls.append(Row(
                [Text(
                    "Total Episode: " + str(series.getTotalEpisode()),
                    size=12,
                    color=ft.colors.YELLOW_700,
                    text_align=ft.TextAlign.CENTER,
                    weight=ft.FontWeight.BOLD,
                )],
                width=1200,
                alignment=ft.MainAxisAlignment.CENTER
            ))

        # add rating and time reviewed
        if series.status == "Reviewed":
            rating_row = Row(
                width=1200,
                alignment=ft.MainAxisAlignment.CENTER,
                vertical_alignment=ft.CrossAxisAlignment.CENTER
            )

            # add rating text
            if series.rating is not None:
                rating_row.controls.append(Text(
                    round(series.getRating(), 2),
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
            if series.comments is not None:
                content.controls.append(
                    Row(
                        [Text(
                            series.comments,
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
            review_date = series.getReviewDate().strftime('%d/%m/%Y')
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
                series.synopsis,
                color=ft.colors.GREEN_400,
                width=1000,
                text_align=ft.TextAlign.JUSTIFY
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
        edit_series_button = ElevatedButton(
            text="Edit Series and Progress",
            on_click=lambda _: self.onclick_edit_series(self.page, series.getID())
        )
        if series.status == "Unwatched":
            edit_series_button.text = "Edit Series and Add Progress"
        button_row.controls.append(edit_series_button)

        content.controls.append(button_row)

        # add episodes
        content.controls.append(Text(
            "Episode List",
            width=1200,
            text_align=ft.TextAlign.CENTER,
            weight=ft.FontWeight.BOLD,
            size=16
        ))

        episode_table = DataTable(
            columns=[
                ft.DataColumn(Text("Episode")),
                ft.DataColumn(Text("Title")),
                ft.DataColumn(Text("Duration")),
                ft.DataColumn(Text("Progress"))
            ]
        )

        content.controls.append(
            Row(
                [episode_table],
                alignment=ft.MainAxisAlignment.CENTER,
                width=1200,
            )
        )
        for episode in series.getEpisodes():
            if episode.episodeProgress is None or episode.episodeProgress == 0:
                progress = "None"
            else:
                progress = Time.seconds_to_hms(episode.episodeProgress)

            episode_table.rows.append(
                ft.DataRow(
                    [ft.DataCell(Text(episode.episodeNumber)),
                     ft.DataCell(Text(episode.title)),
                     ft.DataCell(Text(Time.seconds_to_hms(episode.duration))),
                     ft.DataCell(Text(progress)),
                     ]
                )
            )

        edit_episodes_button = ElevatedButton(
            "Edit episodes and progress",
            on_click=lambda _: self.page.go('edit_episode/' + str(series.getID()))
        )

        content.controls.append(Row([edit_episodes_button], alignment=ft.MainAxisAlignment.CENTER, width=1200,
                                    height=40))

        wrapper.content = content

        return wrapper
