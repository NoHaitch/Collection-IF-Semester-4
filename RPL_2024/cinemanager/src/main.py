import datetime
import random
import flet as ft
from src.gui.GUI import GUI
from src.database.database import DBConnection
from src.database.dbSelect import DBSelect
from src.item.Film import Film
from src.item.Series import Series
from src.item.Episode import Episode

if __name__ == '__main__':
    DBConnection.create_cinemanager_database()

    # load film
    Film.listFilm = DBSelect.select_all_films()

    # load series
    Series.listSeries = DBSelect.select_all_series()

    placeholder_path = "placeholder.png"

    # temporary content
    for i in range(1, 1111):
        if i % 8 == 0:
            Film(
                i, f"Ciko Film {i} Unwatched", placeholder_path, "Unwatched",
                "Abandoned by his parents and raised by an aunt and uncle, teenager Peter Parker (Andrew Garfield), AKA Spider-Man, is trying to sort out who he is and exactly what his feelings are for his first crush, Gwen Stacy (Emma Stone). When Peter finds a mysterious briefcase that was his father's, he pursues a quest to solve his parents' disappearance. His search takes him to Oscorp and the lab of Dr. Curt Connors (Rhys Ifans), setting him on a collision course with Connors' alter ego, the Lizard.", ["action", "mystery", "history", "cooking", "slice of life"],
                None, None, None, None, 1000 + (5 * i), None,
                                                           )
        elif i % 8 == 1:
            temp = Series(
                i, f"Bagas Series {i} Unwatched", placeholder_path, "Unwatched",
                "Abandoned by his parents and raised by an aunt and uncle, teenager Peter Parker (Andrew Garfield), AKA Spider-Man, is trying to sort out who he is and exactly what his feelings are for his first crush, Gwen Stacy (Emma Stone). When Peter finds a mysterious briefcase that was his father's, he pursues a quest to solve his parents' disappearance. His search takes him to Oscorp and the lab of Dr. Curt Connors (Rhys Ifans), setting him on a collision course with Connors' alter ego, the Lizard.", ["Horror", "romance", "adventure", "mystery"],
                None, None, None, None, 13 + i, None,
                                                           )
            temp.addEpisode(Episode(
                1, "episode1", 500, 300
            ))
            temp.addEpisode(Episode(
                2, "episode2", 500, 300
            ))
            temp.addEpisode(Episode(
                3, "episode3", 500, 300
            ))
            temp.addEpisode(Episode(
                4, "episode4", 500, 300
            ))
        elif i % 8 == 2:
            Film(
                i, f"Farhan Film {i}", placeholder_path, "Ongoing",
                "Abandoned by his parents and raised by an aunt and uncle, teenager Peter Parker (Andrew Garfield), AKA Spider-Man, is trying to sort out who he is and exactly what his feelings are for his first crush, Gwen Stacy (Emma Stone). When Peter finds a mysterious briefcase that was his father's, he pursues a quest to solve his parents' disappearance. His search takes him to Oscorp and the lab of Dr. Curt Connors (Rhys Ifans), setting him on a collision course with Connors' alter ego, the Lizard.", ["action", "romance", "adventure", "mystery"],
                None, None, None, datetime.datetime.now().replace(microsecond=0) - datetime.timedelta(days=random.randint(0, 100)),
                1000 + (5 * i), 55 + (i*5//3),
                )
        elif i % 8 == 3:
            Series(
                i, f"Ciko Series {i}", placeholder_path, "Ongoing",
                "Abandoned by his parents and raised by an aunt and uncle, teenager Peter Parker (Andrew Garfield), AKA Spider-Man, is trying to sort out who he is and exactly what his feelings are for his first crush, Gwen Stacy (Emma Stone). When Peter finds a mysterious briefcase that was his father's, he pursues a quest to solve his parents' disappearance. His search takes him to Oscorp and the lab of Dr. Curt Connors (Rhys Ifans), setting him on a collision course with Connors' alter ego, the Lizard.", ["action", "romance", "adventure", "mystery"],
                None, None, None, datetime.datetime.now().replace(microsecond=0) - datetime.timedelta(days=random.randint(0, 100)),
                13 + i, 5 + (i // 2)
            )
        elif i % 8 == 4:
            Film(
                i, f"Bagas Film {i}", placeholder_path, "Finished",
                "Abandoned by his parents and raised by an aunt and uncle, teenager Peter Parker (Andrew Garfield), AKA Spider-Man, is trying to sort out who he is and exactly what his feelings are for his first crush, Gwen Stacy (Emma Stone). When Peter finds a mysterious briefcase that was his father's, he pursues a quest to solve his parents' disappearance. His search takes him to Oscorp and the lab of Dr. Curt Connors (Rhys Ifans), setting him on a collision course with Connors' alter ego, the Lizard.", ["action", "romance", "adventure", "mystery"],
                None, None, None, datetime.datetime.now().replace(microsecond=0) - datetime.timedelta(days=random.randint(0, 100)),
                1000 + (5 * i), 1000 + (5 * i),
                )
        elif i % 8 == 5:
            Series(
                i, f"Farhan Series {i}", placeholder_path, "Finished",
                "Abandoned by his parents and raised by an aunt and uncle, teenager Peter Parker (Andrew Garfield), AKA Spider-Man, is trying to sort out who he is and exactly what his feelings are for his first crush, Gwen Stacy (Emma Stone). When Peter finds a mysterious briefcase that was his father's, he pursues a quest to solve his parents' disappearance. His search takes him to Oscorp and the lab of Dr. Curt Connors (Rhys Ifans), setting him on a collision course with Connors' alter ego, the Lizard.", ["action", "romance", "adventure", "mystery"],
                None, None, None, datetime.datetime.now().replace(microsecond=0) - datetime.timedelta(days=random.randint(0, 100)),
                13 + i, 13 + i,
                )
        elif i % 8 == 6:
            Film(
                i, f"Kanjut Gadab {i}", placeholder_path, "Reviewed",
                "Abandoned by his parents and raised by an aunt and uncle, teenager Peter Parker (Andrew Garfield), AKA Spider-Man, is trying to sort out who he is and exactly what his feelings are for his first crush, Gwen Stacy (Emma Stone). When Peter finds a mysterious briefcase that was his father's, he pursues a quest to solve his parents' disappearance. His search takes him to Oscorp and the lab of Dr. Curt Connors (Rhys Ifans), setting him on a collision course with Connors' alter ego, the Lizard.", ["action", "romance", "adventure", "mystery"],
                random.randint(0, 50) / 10, "Abandoned by his parents and raised by an aunt and uncle, teenager Peter Parker (Andrew Garfield), AKA Spider-Man, is trying to sort out who he is and exactly what his feelings are for his first crush, Gwen Stacy (Emma Stone). When Peter finds a mysterious briefcase that was his father's, he pursues a quest to solve his parents' disappearance. His search takes him to Oscorp and the lab of Dr. Curt Connors (Rhys Ifans), setting him on a colli", datetime.datetime.now().replace(microsecond=0) - datetime.timedelta(days=random.randint(0, 100)), datetime.datetime.now().replace(microsecond=0) - datetime.timedelta(days=random.randint(0, 100)),
                1000 + (5 * i), 1000 + (5 * i),
                )
        elif i % 8 == 7:
            Series(
                i, f"Kharris Series {i}", placeholder_path, "Reviewed",
                "Abandoned by his parents and raised by an aunt and uncle, teenager Peter Parker (Andrew Garfield), AKA Spider-Man, is trying to sort out who he is and exactly what his feelings are for his first crush, Gwen Stacy (Emma Stone). When Peter finds a mysterious briefcase that was his father's, he pursues a quest to solve his parents' disappearance. His search takes him to Oscorp and the lab of Dr. Curt Connors (Rhys Ifans), setting him on a collision course with Connors' alter ego, the Lizard.", ["action", "romance", "adventure", "mystery"],
                random.randint(0, 50) / 10, None, datetime.datetime.now().replace(microsecond=0) - datetime.timedelta(days=random.randint(0, 100)), datetime.datetime.now().replace(microsecond=0) - datetime.timedelta(days=random.randint(0, 100)),
                13 + i, 13 + i,
                )

    app_gui = GUI()
    ft.app(target=app_gui.main_page)
    