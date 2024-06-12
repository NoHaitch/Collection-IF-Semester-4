import os
import datetime
import shutil
from src.item.Series import Series
from src.database.dbSelect import DBSelect
from src.database.dbInsert import DBInsert
from src.database.dbUpdate import DBUpdate
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
    TextField,
    IconButton,
    TextButton,
    Dropdown,
    FilePicker
)

from src.item.Series import Series
from src.utils import is_float


class SeriesEdit:
    def __init__(self, page, back_button: IconButton, cancel_button: TextButton):
        self.back_button = back_button
        self.cancel_button = cancel_button
        self.title = ""
        self.genre = []
        self.synopsis = ""
        self.total_episode = 0
        self.status = "Unwatched"
        self.poster_path = os.path.abspath(os.path.join(
            os.path.dirname(__file__), '..', '..', 'db', 'poster', 'placeholder.png'))
        self.current_episode = None
        self.last_watch_date = None
        self.page = page

    def series_edit_view(self, series_id: int):
        series = Series.get_series_by_id(series_id)
        if series is None:
            self.page.go('/error')
            return

        self.page.title = "Editing Series: " + series.title
        self.page.views.append(
            self.series_edit_wrapper(series)
        )

    def series_edit_wrapper(self, series):
        self.title = series.title
        self.genre = series.genre
        self.status = series.status
        self.poster_path = series.posterPath
        self.current_episode = series.currentEpisode
        self.last_watch_date = series.lastWatch
        self.total_episode = series.totalEpisode

        view = View(
            scroll=ft.ScrollMode.AUTO,
            route='/edit_series/' + str(series.getID()),
            controls=[
                CupertinoAppBar(
                    leading=self.back_button,
                ), self.series_edit_content(series)
            ],
            spacing=26
        )

        return view

    def series_edit_content(self, series):
        self.status = series.status
        wrapper = Row(
            alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )

        content = Column(
            alignment=ft.MainAxisAlignment.CENTER
        )

        content_row = Row(
            alignment=ft.MainAxisAlignment.CENTER
        )

        content_left = Column(
            alignment=ft.MainAxisAlignment.CENTER,
            width=300,
        )

        content_right = Column(
            width=800
        )

        # add page title
        content.controls.append(Row(
            [Text(
                "Editing Series: " + series.title,
                size=18,
                text_align=ft.TextAlign.CENTER,
                weight=ft.FontWeight.BOLD
            )],
            width=1200,
            height=70,
            alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        ))

        # CREATING PROGRESS CONTENT
        # Current Episode progress
        series_progress_row = Row(width=1200, alignment=ft.MainAxisAlignment.START)

        series_progress_row.controls.append(Text(
            "Current Episode Progress:",
            size=18,
            color=ft.colors.ORANGE_ACCENT_400,
            text_align=ft.TextAlign.RIGHT,
            width=150
        ))
        current_episode_field = TextField(
            border_color=ft.colors.ORANGE_ACCENT_400,
            hint_text="",
            hint_style=ft.TextStyle(color=ft.colors.GREY_700, size=14),
            text_size=16,
            width=650
        )
        if self.status == "Ongoing":
            current_episode_field.value = str(series.currentEpisode)
        series_progress_row.controls.append(current_episode_field)

        # CREATING REVIEW CONTENT
        # rating input
        rating_row = Row(
            width=1200,
        )
        rating_row.controls.append(Text(
            "Series Rating\n(0 - 5)",
            size=18,
            color=ft.colors.PINK_ACCENT_400,
            text_align=ft.TextAlign.RIGHT,
            width=150
        ))
        rating_field = TextField(
            border_color=ft.colors.PINK_ACCENT_400,
            hint_text="4.3",
            hint_style=ft.TextStyle(color=ft.colors.GREY_700, size=14),
            text_size=16,
            width=200
        )
        if series.status == "Reviewed" and series.rating is not None:
            rating_field.value = series.rating
        rating_row.controls.append(rating_field)

        # comment input
        comment_row = Row(
            width=1200,
        )
        comment_row.controls.append(Text(
            "Comment",
            size=18,
            color=ft.colors.PINK_ACCENT_400,
            text_align=ft.TextAlign.RIGHT,
            width=150,
        ))
        comment_field = TextField(
            border_color=ft.colors.PINK_ACCENT_400,
            hint_text="Series is amazing!! Would watch again",
            hint_style=ft.TextStyle(color=ft.colors.GREY_700, size=14),
            text_size=16,
            width=650,
            multiline=True,
            min_lines=3,
            max_lines=3
        )
        if series.status == "Reviewed" and series.comments is not None:
            comment_field.value = series.comments
        comment_row.controls.append(comment_field)

        # status dropdown onchange
        def on_dropdown_change_status(on_change_control: ft.ControlEvent):
            self.status = on_change_control.control.value
            progress_content_col.clean()
            review_content_col.clean()
            error_text.value = ""

            if self.status == "Ongoing":
                # add progress field
                progress_content_col.controls.append(
                    Text(
                        "Series Progress",
                        size=18,
                        color=ft.colors.ORANGE_ACCENT_400,
                        weight=ft.FontWeight.BOLD,
                        text_align=ft.TextAlign.CENTER,
                        width=1200,
                        height=40
                    )
                )
                progress_content_col.controls.append(series_progress_row)

            elif dropdown.value == "Reviewed":
                # add progress field
                review_content_col.controls.append(
                    Text(
                        "Series Review",
                        size=18,
                        color=ft.colors.PINK_ACCENT_400,
                        weight=ft.FontWeight.BOLD,
                        text_align=ft.TextAlign.CENTER,
                        width=1200,
                        height=40
                    )
                )

                review_content_col.controls.append(rating_row)
                review_content_col.controls.append(comment_row)

            progress_content_col.update()
            review_content_col.update()
            content.update()

        # status dropdown
        dropdown = Dropdown(
            width=200,
            label="Status",
            value=series.status,
            hint_style=ft.TextStyle(
                color=ft.colors.GREEN_ACCENT_400,
                weight=ft.FontWeight.BOLD,
                size=14,
            ),
            label_style=ft.TextStyle(
                color=ft.colors.GREEN_ACCENT_400,
                weight=ft.FontWeight.BOLD,
                size=14,
            ),
            options=[
                ft.dropdown.Option("Unwatched"),
                ft.dropdown.Option("Ongoing"),
                ft.dropdown.Option("Finished"),
                ft.dropdown.Option("Reviewed")
            ],
            color=ft.colors.GREEN_ACCENT_400,
            text_style=ft.TextStyle(weight=ft.FontWeight.BOLD),
            alignment=ft.alignment.center,
            on_change=on_dropdown_change_status
        )

        status_dropdown = Row(
            [dropdown],
            width=1200,
            height=100,
            alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.CrossAxisAlignment.CENTER
        )
        content.controls.append(status_dropdown)

        # Title input
        title_row = Row(
            width=800,
        )
        title_row.controls.append(Text(
            "Series Title",
            size=18,
            color=ft.colors.GREEN_ACCENT_400,
            text_align=ft.TextAlign.RIGHT,
            width=150
        ))
        title_field = TextField(
            border_color=ft.colors.GREEN_ACCENT_400,
            hint_text="The Amazing Bear",
            value=series.title,
            hint_style=ft.TextStyle(color=ft.colors.GREY_700, size=14),
            text_size=16,
            width=650
        )
        title_row.controls.append(title_field)
        content_right.controls.append(title_row)

        # Genre input
        genre_text = ""
        for i in range(0, len(series.genre)):
            genre_text += series.genre[i]
            if i != len(series.genre) - 1:
                genre_text += ", "

        genre_row = Row(
            width=800
        )
        genre_row.controls.append(Text(
            "Genre",
            size=18,
            color=ft.colors.GREEN_ACCENT_400,
            text_align=ft.TextAlign.RIGHT,
            width=150
        ))
        genre_field = TextField(
            border_color=ft.colors.GREEN_ACCENT_400,
            hint_text="Action, Romance, Horror",
            hint_style=ft.TextStyle(color=ft.colors.GREY_700, size=14),
            text_size=14,
            width=650,
        )
        genre_field.value = genre_text
        genre_row.controls.append(genre_field)
        content_right.controls.append(genre_row)

        # Synopsis input
        synopsis_row = Row(
            width=800
        )
        synopsis_row.controls.append(Text(
            "Synopsis",
            size=18,
            color=ft.colors.GREEN_ACCENT_400,
            text_align=ft.TextAlign.RIGHT,
            width=150
        ))
        synopsis_field = TextField(
            border_color=ft.colors.GREEN_ACCENT_400,
            hint_text="During World War II, Lt. Gen. Leslie Groves Jr. appoints "
                      "physicist J. Robert Oppenheimer to work on the top-secret "
                      "Manhattan Project. Oppenheimer and a team of scientists spend "
                      "years developing and designing the atomic bomb. Their work comes "
                      "to fruition on July 16, 1945, as they witness the world's first "
                      "nuclear explosion, forever changing the course of history.",
            hint_style=ft.TextStyle(color=ft.colors.GREY_700, size=14),
            value=series.synopsis,
            text_size=14,
            width=650,
            multiline=True,
            min_lines=4,
            max_lines=4,
        )

        synopsis_row.controls.append(synopsis_field)
        content_right.controls.append(synopsis_row)

        # Series duration input
        series_episode_row = Row(width=1200, alignment=ft.MainAxisAlignment.START)

        series_episode_row.controls.append(Text(
            "Number Episode to Edit:",
            size=18,
            color=ft.colors.GREEN_ACCENT_400,
            text_align=ft.TextAlign.RIGHT,
            width=150
        ))
        total_episode_field = TextField(
            border_color=ft.colors.GREEN_ACCENT_400,
            hint_text="21",
            hint_style=ft.TextStyle(color=ft.colors.GREY_700, size=14),
            text_size=16,
            width=650,
            value=series.totalEpisode
        )
        series_episode_row.controls.append(total_episode_field)
        content_right.controls.append(series_episode_row)

        # Poster
        poster_column = Column(
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )

        self.poster_path = series.posterPath
        poster_img = Image(
            src=self.poster_path,
            width=240,
            height=360
        )

        poster_column.controls.append(poster_img)

        # pick_file_result
        def pick_file_result(e: ft.FilePickerResultEvent, poster_img: Image):
            if e.files:
                selected_files.value = e.files[0].name
                self.poster_path = e.files[0].path
                poster_img.src = self.poster_path
                poster_img.update()
            selected_files.update()

        def reset_file(e, poster_img: Image):
            self.poster_path = os.path.abspath(os.path.join(
                os.path.dirname(__file__), '..', '..', 'db', 'poster', 'placeholder.png'))
            poster_img.src = self.poster_path
            poster_img.update()
            selected_files.value = "Placeholder"
            selected_files.update()

        pick_file_dialog = FilePicker(on_result=lambda e: pick_file_result(e, poster_img))
        selected_files = Text(series.posterPath.split('\\')[-1], text_align=ft.TextAlign.CENTER, width=300)
        content.controls.append(pick_file_dialog)
        content.controls.append(selected_files)
        poster_buttons = Row(
            [ElevatedButton(
                "Pick files",
                icon=ft.icons.UPLOAD_FILE,
                on_click=lambda _: pick_file_dialog.pick_files(
                    allow_multiple=False,
                    allowed_extensions=['jpg', 'jpeg', 'png', 'gif']
                ),
            ), ElevatedButton(
                "Reset",
                on_click=lambda e: reset_file(e, poster_img),
            )],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=10
        )
        poster_column.controls.append(poster_buttons)
        content_left.controls.append(poster_column)
        content_row.controls.append(content_left)
        content_row.controls.append(content_right)
        content.controls.append(content_row)

        progress_content_col = Column(
            width=1200,
        )
        review_content_col = Column(
            width=1200
        )

        if self.status == "Ongoing":
            # add progress field
            progress_content_col.controls.append(
                Text(
                    "Series Progress",
                    size=18,
                    color=ft.colors.ORANGE_ACCENT_400,
                    weight=ft.FontWeight.BOLD,
                    text_align=ft.TextAlign.CENTER,
                    width=1200,
                    height=40
                )
            )
            progress_content_col.controls.append(series_progress_row)

        elif dropdown.value == "Reviewed":
            # add progress field
            review_content_col.controls.append(
                Text(
                    "Series Review",
                    size=18,
                    color=ft.colors.PINK_ACCENT_400,
                    weight=ft.FontWeight.BOLD,
                    text_align=ft.TextAlign.CENTER,
                    width=1200,
                    height=40
                )
            )
            review_content_col.controls.append(rating_row)
            review_content_col.controls.append(comment_row)

        content.controls.append(Row([progress_content_col], width=1200))
        content.controls.append(Row([review_content_col], width=1200))

        # submit button
        def onsubmit(e: ft.ControlEvent):
            current_episode = -1
            rating = -1

            if title_field.value == "":
                error_text.value = "Title is empty!"
                error_text.update()
                return
            if genre_field.value == "":
                error_text.value = "Genre is empty!"
                error_text.update()
                return
            if synopsis_field.value == "":
                error_text.value = "Synopsis is empty!"
                error_text.update()
                return
            if total_episode_field.value == "":
                error_text.value = "Total episode is empty!"
                error_text.update()
                return

            # proses total episode
            if str(total_episode_field.value).isnumeric():
                total_episode = int(total_episode_field.value)
                if total_episode <= 0:
                    error_text.value = "Total Episode must at least be one"
                    error_text.update()
                    return
            else:
                error_text.value = "Total Episode is not valid!"
                error_text.update()
                return

            if self.status == "Ongoing":
                # proses total episode
                if str(current_episode_field.value).isnumeric():
                    current_episode = int(current_episode_field.value)
                    if current_episode < 0:
                        error_text.value = "Current Episode is not valid"
                        error_text.update()
                        return
                else:
                    error_text.value = "Current Episode is not valid!"
                    error_text.update()
                    return
                if current_episode > total_episode:
                    error_text.value = "Current Episode is Further that the Total Episode!"
                    error_text.update()
                    return
                elif current_episode == total_episode:
                    error_text.value = ("Current Episode is Further that the Total Episode!\n "
                                        "Change the status to finished if the series is already fully watched")
                    error_text.update()
                    return
            elif self.status == "Finished":
                current_episode = total_episode
            elif self.status == "Reviewed":
                current_episode = total_episode
                if rating_field.value == "" and comment_field.value == "":
                    error_text.value = "Either Rating or Comment must be filled!"
                    error_text.update()
                    return

                if rating_field.value != "" and is_float(rating_field.value):
                    rating = float(rating_field.value)
                    if rating < 0 or rating > 5:
                        error_text.value = "Rating is not valid! Choose a rating between 0 to 5"
                        error_text.update()
                        return
                else:
                    error_text.value = "Rating is not valid! Choose a rating between 0 to 5"
                    error_text.update()
                    return

            # proses genre
            genre = genre_field.value.split(",")
            genre = [elmt.strip() for elmt in genre]

            error_text.value = "New series"
            error_text.color = ft.colors.GREEN_ACCENT_400
            error_text.update()
            error_text.color = ft.colors.RED

            # proses image
            destination_path = series.getPosterPath()
            if self.poster_path != series.getPosterPath():
                splitted = self.poster_path.split('\\')
                file_name = splitted[len(splitted)-1]
                destination_path = os.path.abspath(os.path.join(
                    os.path.dirname(__file__), '..', '..', 'db', 'poster', file_name))
                os.remove(series.getPosterPath())
                shutil.copy(self.poster_path, destination_path)

            print("Edit Series: ")
            print(" > Status: ", self.status.lower())
            print(" > Title: ", title_field.value)
            print(" > PosterPath: ", self.poster_path)
            print(" > Genre: ", genre)
            print(" > Synopsis: ", synopsis_field.value)
            print(" > Total Episode: ", total_episode)
            print(" > Progress Duration: ", current_episode)
            print(" > Last watched: ", datetime.datetime.now().replace(microsecond=0))
            print(" > Rating: ", rating)
            print(" > Comment: ", comment_field.value)

            # TODO: EDIT SERIES TO DATABASE
            if series.getTitle() != title_field.value or series.getTotalEpisode() != total_episode:
                if DBSelect.check_series_by_title_episodes(title_field.value, total_episode):
                    error_text.value = "Updated Series is another film that exist"
                    error_text.update()
                    return
            new_series = Series(
                series.getID(), title_field.value, destination_path, self.status, synopsis_field.value, genre,
                None, None, None, None, total_episode, None, []
            )
            DBUpdate.update_series_data(new_series)

            if self.status == "Ongoing" or self.status == "Reviewed" or self.status == "Finished":
                new_series.setTotalEpisode(total_episode)
                new_series.setLastWatch(datetime.datetime.now().replace(microsecond=0))
                new_series.setStatus(self.status)
                DBUpdate.update_watch_item_status(new_series.getID(), self.status)
                DBUpdate.update_watch_item_date_watched(new_series.getID(), new_series.getLastWatch())
                DBUpdate.update_series_progress(new_series.getID(), new_series.getTotalEpisode())

            if self.status == "Reviewed":
                new_series.setRating(rating)
                new_series.setComments(comment_field.value)
                new_series.setReviewDate(datetime.datetime.now().replace(microsecond=0))
                if new_series.getStatus() == "Reviewed":
                    DBUpdate.update_review(new_series)
                else:
                    DBInsert.insert_review(new_series)

            Series.listSeries.remove(series)

            self.page.go('/series/' + str(series.getID()))

        submit_button = ElevatedButton(
            text="Finish Editing",
            on_click=onsubmit
        )

        content.controls.append(
            Row(
                [submit_button, self.cancel_button],
                alignment=ft.MainAxisAlignment.CENTER,
                width=1200
            )
        )

        # error text
        error_text = Text(
            "",
            text_align=ft.TextAlign.CENTER,
            color=ft.colors.RED,
            size=16,
            width=1200,
            weight=ft.FontWeight.BOLD
        )

        content.controls.append(error_text)

        wrapper.controls.append(content)

        return Container(
            content=wrapper,
            padding=ft.Padding(top=30, left=0, bottom=0, right=0)
        )
