import os
import sqlite3
import datetime
from src.database.dbSelect import DBSelect
from src.item.Film import Film
from src.item.Series import Series
from src.item.WatchItem import WatchItem
from src.item.Episode import Episode


class DBInsert:
    """
    Insert into SQLite Database
    """

    @staticmethod
    def insert_review(watch_item: WatchItem):
        """
        SQL query to insert a new film into Film table

        :param watch_item: WatchItem
        """
        db_file = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'db', 'cinemanager.db'))
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()

        cursor.execute(f"""INSERT INTO Review
        (id_item, rating, date_review, comment)
        VALUES ({watch_item.getID()}, {watch_item.getRating()},
                '{watch_item.getReviewDate()}', '{watch_item.getComments()}')
        """)
        conn.commit()

        conn.close()

    @staticmethod
    def insert_a_genre(new_genre : str, conn : sqlite3.Connection, watch_item_id : int, genre_set = None):
        """
        SQL query to insert a single genre for a WatchItem

        :param conn:
        :param watch_item_id:
        :param new_genre: str
        :param genre_set: None
        """
        if genre_set is None:
            genre_list = DBSelect.get_all_genres()
            genre_set = set()
            if genre_list is not None:
                genre_set = set(genre_list)

        cursor = conn.cursor()
        _genre_id = 0
        if new_genre not in genre_set:
            genre_set.add(new_genre)
            cursor.execute(f""" INSERT INTO Genre (genre_name) 
                                VALUES ('{new_genre}') 
                            """)
            conn.commit()

            _genre_id = cursor.lastrowid
        else:
            cursor.execute(f"""SELECT genre_id FROM Genre 
                        WHERE genre_name = '{new_genre}'
                        """)
            _genre_id = cursor.fetchone()[0]

        cursor.execute(f""" INSERT INTO Categorize (id_item, genre_id) 
                            VALUES ({watch_item_id}, {_genre_id}) 
                        """)
        conn.commit()

    @staticmethod
    def insert_new_genres(new_genres : list[str], conn : sqlite3.Connection, watch_item_id : int):
        """
        SQL query to insert a new list of genres for a certain WatchItem

        :param conn:
        :param watch_item_id:
        :param new_genres: list[str]
        """
        genre_list = DBSelect.get_all_genres()
        genre_set = set()
        if genre_list is not None:
            genre_set = set(genre_list)

        for genre in new_genres:
            DBInsert.insert_a_genre(genre, conn, watch_item_id, genre_set)

    @staticmethod
    def insert_film(new_film: Film):
        """
        SQL query to insert a new film into Film table

        :param new_film: Film
        """
        db_file = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'db', 'cinemanager.db'))
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()

        cursor.execute(f"""INSERT INTO WatchItem
                           (title, poster, synopsis, status, date_watched) 
                           VALUES ('{new_film.getTitle()}', '{new_film.getPosterPath()}', '{new_film.getSynopsis()}', 
                           'Unwatched', NULL)
                        """)
        conn.commit()

        foreign_key = cursor.lastrowid
        cursor.execute(f"""INSERT INTO Film
                           (id_item, duration_film, duration_progress) 
                           VALUES ({foreign_key}, {new_film.duration}, 0)
                        """)
        DBInsert.insert_new_genres(new_film.getGenre(), conn, foreign_key)
        conn.commit()

        conn.close()

    @staticmethod
    def test_insert_film() -> bool:
        """
        Test whether a Film can be inserted to database

        Returns:
            bool: True if the insertion was successful, False otherwise.
        """
        dull_genre = ['Thriller', 'Action', 'Horror']
        dt = datetime.datetime(2022, 5, 13, 12, 30, 45)
        film1 = Film(1, 'Dune: part 2', 'None', 'Reviewed', 'Paul Atreides is Lisan Al-Ghaib',
                     dull_genre, 5, 'AS WRITTEN', dt, dt, 10800, 10800)
        film2 = Film(2, 'Drive', 'None', 'Finished', 'Ryan Gosling is literally me',
                     dull_genre, None, None, None, dt, 7200, 7200)
        film3 = Film(3, 'Bagas Dribbel', 'None', 'Unwatched', 'POV jadi anak basket di sekolah',
                     dull_genre, None, None, None, None, 7200, 0)

        DBInsert.insert_film(film1)
        DBInsert.insert_review(film1)
        DBInsert.insert_film(film2)
        DBInsert.insert_film(film3)

        db_file = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'db', 'cinemanager.db'))
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()

        cursor.execute(f"""SELECT title FROM WatchItem
                        """)
        res_list = cursor.fetchall()

        assert res_list[0][0] == film1.getTitle()
        assert res_list[1][0] == film2.getTitle()
        assert res_list[2][0] == film3.getTitle()

        conn.commit()
        conn.close()
        return True

    @staticmethod
    def insert_series(new_series: Series):
        """
        SQL query to insert a new series into Series table

        :param new_series : Series
        """
        db_file = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'db', 'cinemanager.db'))
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()


        cursor.execute(f"""INSERT INTO WatchItem
                           (title, poster, synopsis, status, date_watched) 
                           VALUES ('{new_series.getTitle()}', '{new_series.getPosterPath()}', '{new_series.getSynopsis()}', 
                           'Unwatched', NULL)
                        """)
        conn.commit()

        foreign_key = cursor.lastrowid
        cursor.execute(f"""INSERT INTO Series
                           (id_item, total_episode, current_episode) 
                           VALUES ({foreign_key}, {new_series.totalEpisode}, 1)
                        """)
        conn.commit()

        DBInsert.insert_new_genres(new_series.getGenre(), conn, foreign_key)

        conn.close()

    @staticmethod
    def test_insert_series() -> bool:
        """
        Test whether a Series can be inserted to database

        Returns:
            bool: True if the insertion was successful, False otherwise.
        """
        dull_genre = ['Comedy', 'SciFi']
        dt = datetime.datetime(2022, 5, 13, 12, 30, 45)
        series1 = Series(4, 'Atlanta', 'None', 'Reviewed', 'all about that Paperboy',
                     dull_genre, 5, 'Darius Weird', dt, dt, 40, 40, None)
        ep1 = Episode(1, 'White Christmas', 1800, 1800)
        ep2 = Episode(2, 'Black Museum', 3600, 3600)
        ep3 = Episode(3, 'Bandersnatch', 1200, 3600)
        BM_episodes = [ep1, ep2, ep3]
        series2 = Series(5, 'Black Mirror', 'None', 'Finished', 'Technology bad',
                     dull_genre, None, None, None, dt, 10, 10, BM_episodes)
        series3 = Series(6, 'Bagas Dribbel: The Series', 'None', 'Unwatched', 'Bagas Dribbel tapi dijadiin series',
                     dull_genre, None, None, None, None, 100, 0, None)

        DBInsert.insert_series(series1)
        DBInsert.insert_review(series1)
        DBInsert.insert_series(series2)
        DBInsert.insert_new_episodes(series2.getEpisodes(), series2.getID())
        DBInsert.insert_series(series3)

        db_file = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'db', 'cinemanager.db'))
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()

        cursor.execute(f"""SELECT title FROM WatchItem
                        WHERE id_item > 3
                        """)
        res_list = cursor.fetchall()

        assert res_list[0][0] == series1.getTitle()
        assert res_list[1][0] == series2.getTitle()
        assert res_list[2][0] == series3.getTitle()

        conn.close()
        return True

    @staticmethod
    def insert_new_episodes(new_episodes : list[Episode], series_id : int):
        """
        SQL query to insert a new list of episodes for a certain Series

        :param series_id:
        :param new_episodes:
        """
        db_file = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'db', 'cinemanager.db'))
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()

        for episode in new_episodes:
            cursor.execute(f"""INSERT INTO Episode
                               (id_item, episode_number, title, duration_episode, duration_progress)
                               VALUES ({series_id}, {episode.get_episodeNumber()}, '{episode.get_title()}', 
                                {episode.get_duration()}, {episode.get_episodeProgress()})
                            """)
            conn.commit()
        conn.close()
