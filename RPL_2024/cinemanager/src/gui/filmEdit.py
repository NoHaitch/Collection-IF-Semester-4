import os
import datetime
import flet as ft
import shutil
from src.database.dbSelect import DBSelect
from src.database.dbUpdate import DBUpdate
from src.database.dbInsert import DBInsert
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

from src.item.Film import Film
from src.utils import is_float


class FilmEdit:
    def __init__(self, page, back_button: IconButton, cancel_button: TextButton):
        self.back_button = back_button
        self.cancel_button = cancel_button
        self.title = ""
        self.genre = []
        self.synopsis = ""
        self.duration = 0
        self.status = "Unwatched"
        self.poster_path = os.path.abspath(os.path.join(
            os.path.dirname(__file__), '..', '..', 'db', 'poster', 'placeholder.png'))
        self.duration_progress = None
        self.last_watch_date = None
        self.page = page

    def film_edit_view(self, film_id: int):
        film = Film.get_film_by_id(film_id)
        if film is None:
            self.page.go('/error')
            return

        self.page.title = "Editing Film: " + film.title
        self.page.views.append(
            self.film_edit_wrapper(film)
        )

    def film_edit_wrapper(self, film):
        self.title = film.title
        self.genre = film.genre
        self.status = film.status
        self.poster_path = film.posterPath
        self.duration_progress = film.progress
        self.last_watch_date = film.lastWatch
        self.duration = film.duration

        view = View(
            scroll=ft.ScrollMode.AUTO,
            route='/edit_film/' + str(film.getID()),
            controls=[
                CupertinoAppBar(
                    leading=self.back_button,
                ), self.film_edit_content(film)
            ],
            spacing=26
        )

        return view

    def film_edit_content(self, film : Film):
        self.status = film.status
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
                "Editing Film: " + film.title,
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
        # Duration progress
        film_progress_row = Row(width=1200, alignment=ft.MainAxisAlignment.START)

        film_progress_row.controls.append(Text(
            "Progress Duration:",
            size=18,
            color=ft.colors.ORANGE_ACCENT_400,
            text_align=ft.TextAlign.RIGHT,
            width=250
        ))
        # Hours
        film_progress_row.controls.append(Text(
            "Hour",
            size=18,
            color=ft.colors.GREY_700,
            text_align=ft.TextAlign.RIGHT,
        ))
        progress_hour_field = TextField(
            border_color=ft.colors.ORANGE_ACCENT_400,
            hint_text="00",
            hint_style=ft.TextStyle(color=ft.colors.GREY_700, size=14),
            text_size=14,
            width=50
        )

        progress_minute_field = TextField(
            border_color=ft.colors.ORANGE_ACCENT_400,
            hint_text="00",
            hint_style=ft.TextStyle(color=ft.colors.GREY_700, size=14),
            text_size=14,
            width=50
        )

        progress_second_field = TextField(
            border_color=ft.colors.ORANGE_ACCENT_400,
            hint_text="00",
            hint_style=ft.TextStyle(color=ft.colors.GREY_700, size=14),
            text_size=14,
            width=50
        )
        if film.progress is not None:
            seconds = self.duration_progress
            progress_hour_field.value = seconds // 3600
            seconds = seconds % 3600
            progress_minute_field.value = seconds // 60
            seconds = seconds % 60
            progress_second_field.value = seconds

        film_progress_row.controls.append(progress_hour_field)
        # Minute
        film_progress_row.controls.append(Text(
            "Minute",
            size=18,
            color=ft.colors.GREY_700,
            text_align=ft.TextAlign.RIGHT,
        ))
        film_progress_row.controls.append(progress_minute_field)
        # Seconds
        film_progress_row.controls.append(Text(
            "Second",
            size=18,
            color=ft.colors.GREY_700,
            text_align=ft.TextAlign.RIGHT,
        ))
        film_progress_row.controls.append(progress_second_field)

        # CREATING REVIEW CONTENT
        # rating input
        rating_row = Row(
            width=1200,
        )
        rating_row.controls.append(Text(
            "Film Rating\n(0 - 5)",
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
        if film.status == "Reviewed" and film.rating is not None:
            rating_field.value = film.rating
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
            hint_text="Film is amazing!! Would watch again",
            hint_style=ft.TextStyle(color=ft.colors.GREY_700, size=14),
            text_size=16,
            width=650,
            multiline=True,
            min_lines=3,
            max_lines=3
        )
        if film.status == "Reviewed" and film.comments is not None:
            comment_field.value = film.comments
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
                        "Film Progress",
                        size=18,
                        color=ft.colors.ORANGE_ACCENT_400,
                        weight=ft.FontWeight.BOLD,
                        text_align=ft.TextAlign.CENTER,
                        width=1200,
                        height=40
                    )
                )
                progress_content_col.controls.append(film_progress_row)
            elif dropdown.value == "Reviewed":
                # add progress field
                review_content_col.controls.append(
                    Text(
                        "Film Review",
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
            value=film.status,
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
            "Film Title",
            size=18,
            color=ft.colors.GREEN_ACCENT_400,
            text_align=ft.TextAlign.RIGHT,
            width=150
        ))
        title_field = TextField(
            border_color=ft.colors.GREEN_ACCENT_400,
            hint_text="The Amazing Bear",
            value=film.title,
            hint_style=ft.TextStyle(color=ft.colors.GREY_700, size=14),
            text_size=16,
            width=650
        )
        title_row.controls.append(title_field)
        content_right.controls.append(title_row)

        # Genre input
        genre_text = ""
        for i in range(0, len(film.genre)):
            genre_text += film.genre[i]
            if i != len(film.genre) - 1:
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
            value=film.synopsis,
            text_size=14,
            width=650,
            multiline=True,
            min_lines=4,
            max_lines=4,
        )

        synopsis_row.controls.append(synopsis_field)
        content_right.controls.append(synopsis_row)

        # Film duration input
        film_row = Row()

        film_row.controls.append(Text(
            "Film Duration:",
            size=18,
            color=ft.colors.GREEN_ACCENT_400,
            text_align=ft.TextAlign.RIGHT,
            width=150
        ))

        hour_field = TextField(
            border_color=ft.colors.GREEN_ACCENT_400,
            hint_text="00",
            hint_style=ft.TextStyle(color=ft.colors.GREY_700, size=14),
            text_size=14,
            width=50
        )

        minute_field = TextField(
            border_color=ft.colors.GREEN_ACCENT_400,
            hint_text="00",
            hint_style=ft.TextStyle(color=ft.colors.GREY_700, size=14),
            text_size=14,
            width=50
        )

        second_field = TextField(
            border_color=ft.colors.GREEN_ACCENT_400,
            hint_text="00",
            hint_style=ft.TextStyle(color=ft.colors.GREY_700, size=14),
            text_size=14,
            width=50
        )

        seconds = self.duration
        hour_field.value = seconds // 3600
        seconds = seconds % 3600
        minute_field.value = seconds // 60
        seconds = seconds % 60
        second_field.value = seconds
        # Hours
        film_row.controls.append(Text(
            "Hour",
            size=18,
            color=ft.colors.GREY_700,
            text_align=ft.TextAlign.RIGHT,
        ))
        film_row.controls.append(hour_field)
        # Minute
        film_row.controls.append(Text(
            "Minute",
            size=18,
            color=ft.colors.GREY_700,
            text_align=ft.TextAlign.RIGHT,
        ))
        film_row.controls.append(minute_field)
        # Seconds
        film_row.controls.append(Text(
            "Second",
            size=18,
            color=ft.colors.GREY_700,
            text_align=ft.TextAlign.RIGHT,
        ))
        film_row.controls.append(second_field)
        content_right.controls.append(film_row)

        # Poster
        poster_column = Column(
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )

        self.poster_path = film.posterPath
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
        selected_files = Text(film.posterPath.split('\\')[-1], text_align=ft.TextAlign.CENTER, width=300)
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
                    "Film Progress",
                    size=18,
                    color=ft.colors.ORANGE_ACCENT_400,
                    weight=ft.FontWeight.BOLD,
                    text_align=ft.TextAlign.CENTER,
                    width=1200,
                    height=40
                )
            )
            progress_content_col.controls.append(film_progress_row)

        elif dropdown.value == "Reviewed":
            # add progress field
            review_content_col.controls.append(
                Text(
                    "Film Review",
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
            progress_duration = None
            rating = None

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
            if hour_field.value == "":
                error_text.value = "Hour is empty!"
                error_text.update()
                return
            if minute_field.value == "":
                error_text.value = "Minute is empty!"
                error_text.update()
                return
            if second_field.value == "":
                error_text.value = "Second is empty!"
                error_text.update()
                return

                # proses duration
            if (str(hour_field.value).isnumeric() and str(minute_field.value).isnumeric()
                    and str(second_field.value).isnumeric()):
                hour = int(hour_field.value)
                minute = int(minute_field.value)
                second = int(second_field.value)
                if hour > 24 or hour < 0 or minute > 59 or minute < 0 or second > 59 or second < 0:
                    error_text.value = "Duration is not valid"
                    error_text.update()
                    return
            else:
                error_text.value = "Duration is not valid!"
                error_text.update()
                return

            duration = (hour * 60 * 60)
            duration += (minute * 60)
            duration += second

            if self.status == "Ongoing":
                if progress_hour_field.value == "":
                    error_text.value = "Progress Hour is empty!"
                    error_text.update()
                    return
                if progress_minute_field.value == "":
                    error_text.value = "Progress Minute is empty!"
                    error_text.update()
                    return
                if progress_second_field.value == "":
                    error_text.value = "Progress Second is empty!"
                    error_text.update()
                    return

                # proses duration
                if (str(progress_hour_field.value).isnumeric() and
                        str(progress_minute_field.value).isnumeric() and
                        str(progress_second_field.value).isnumeric()):
                    progress_hour = int(progress_hour_field.value)
                    progress_minute = int(progress_minute_field.value)
                    progress_second = int(progress_second_field.value)
                    if (progress_hour > 24 or progress_hour < 0 or
                            progress_minute > 59 or progress_minute < 0 or
                            progress_second > 59 or progress_second < 0):
                        error_text.value = "Progress Duration is not valid"
                        error_text.update()
                        return
                else:
                    error_text.value = "Progress Duration is not valid!"
                    error_text.update()
                    return

                progress_duration = (progress_hour * 60 * 60)
                progress_duration += (progress_minute * 60)
                progress_duration += progress_second

                if progress_duration > duration:
                    error_text.value = "Progress Duration is Further that the film Duration!"
                    error_text.update()
                    return
                elif progress_duration == duration:
                    error_text.value = ("Progress Duration is the same as the film Duration!\n "
                                        "Change the status to finished if the film is already fully watched")
                    error_text.update()
                    return
            elif self.status == "Finished":
                progress_duration = duration
            elif self.status == "Reviewed":
                progress_duration = duration
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

                progress_duration = duration

            # proses genre
            genre = genre_field.value.split(",")
            genre = [elmt.strip() for elmt in genre]

            error_text.value = "New film"
            error_text.color = ft.colors.GREEN_ACCENT_400
            error_text.update()
            error_text.color = ft.colors.RED

            # proses image
            destination_path = film.getPosterPath()
            if self.poster_path != film.getPosterPath():
                splitted = self.poster_path.split('\\')
                file_name = splitted[len(splitted)-1]
                destination_path = os.path.abspath(os.path.join(
                    os.path.dirname(__file__), '..', '..', 'db', 'poster', file_name))
                os.remove(film.getPosterPath())
                shutil.copy(self.poster_path, destination_path)

            print("Edit Film: ")
            print(" > Status: ", self.status.lower())
            print(" > Title: ", title_field.value)
            print(" > PosterPath: ", self.poster_path)
            print(" > Genre: ", genre)
            print(" > Synopsis: ", synopsis_field.value)
            print(" > Duration: ", duration)
            print(" > Progress Duration: ", progress_duration)
            print(" > Last watched: ", datetime.datetime.now().replace(microsecond=0))
            print(" > Rating: ", rating)
            print(" > Comment: ", comment_field.value)

            # EDIT FILM TO DATABASE
            if film.getTitle() != title_field.value or film.getDuration() != duration:
                if DBSelect.check_film_by_title_duration(title_field.value, duration):
                    error_text.value = "Updated Film is another film that exist"
                    error_text.update()
                    return
            new_film = Film(
                film.getID(), title_field.value, destination_path, self.status, synopsis_field.value, genre,
                None, None, None, None, duration, None
            )
            DBUpdate.update_film_data(new_film)

            if self.status == "Ongoing" or self.status == "Reviewed" or self.status == "Finished":
                new_film.setProgress(progress_duration)
                new_film.setLastWatch(datetime.datetime.now().replace(microsecond=0))
                new_film.setStatus(self.status)
                DBUpdate.update_watch_item_status(new_film.getID(), self.status)
                DBUpdate.update_watch_item_date_watched(new_film.getID(), new_film.getLastWatch())
                DBUpdate.update_film_progress(new_film.getID(), new_film.getProgress())

            if self.status == "Reviewed":
                new_film.setRating(rating)
                new_film.setComments(comment_field.value)
                new_film.setReviewDate(datetime.datetime.now().replace(microsecond=0))
                if film.getStatus() == "Reviewed":
                    DBUpdate.update_review(new_film)
                else:
                    DBInsert.insert_review(new_film)

            Film.listFilm.remove(film)
            """
            for film_item in Film.listFilm:
                if film_item.getTitle() == film.getTitle() and film_item.getDuration() == film.getDuration():
                    Film.listFilm.remove(film)
                    break
            """
            self.page.go('/film/' + str(film.getID()))

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
