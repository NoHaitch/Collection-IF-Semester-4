import os
import sqlite3
from datetime import datetime
from src.item.Film import Film
from src.item.Series import Series
from src.item.Episode import Episode

class DBSelect:
    """
    Select data from SQLite Database
    """

    @staticmethod
    def get_review_by_id(_id: int, conn: sqlite3.Connection):
        """
        SQL query to select a review based on WatchItem id

        Returns:
            Tuple of review (rating, comments, review_date)
        """
        cursor = conn.cursor()
        cursor.execute(f"""SELECT rating, comment, date_review
                        FROM Review
                        WHERE id_item = {_id}
                        """)
        res = cursor.fetchone()
        if res is None:
            return (None, None, None)
        else:
            res = list(res)
            res[2] = datetime.strptime(res[2], '%Y-%m-%d %H:%M:%S')
            return res

    @staticmethod
    def get_all_genres():
        """
        SQL query to select all genres from genre table

        Returns:
            List of string (genres)
        """
        db_file = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'db', 'cinemanager.db'))
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()

        cursor.execute(f"""SELECT genre_name
                        FROM Genre
                        """)

        res = cursor.fetchall()

        conn.close()

        if res is None:
            return None
        else:
            res_list = []
            for dirty in res:
                res_list.append(dirty[0])
            return res_list

    @staticmethod
    def get_genres_by_id(_id : int, conn : sqlite3.Connection):
        """
        SQL query to select all genres of a WatchItem by its id

        Returns:
            List of string (genres)
        """

        cursor = conn.cursor()

        cursor.execute(f"""SELECT Genre.genre_name
                        FROM Genre INNER JOIN Categorize on Genre.genre_id = Categorize.genre_id
                        WHERE id_item = '{_id}'
                        """)

        res = cursor.fetchall()

        genre_list = []
        if res is None:
            return None
        else:
            for genre in res:
                genre_list.append(genre[0])
            return genre_list

    @staticmethod
    def select_film_by_id(_id: int):
        """
        SQL query to select a film from Film table based on film id

        Returns:
            Film object if found, None otherwise
        """

        db_file = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'db', 'cinemanager.db'))
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()

        cursor.execute(f"""SELECT 
                        WatchItem.id_item, title, poster, status, synopsis, 
                        date_watched, duration_film, duration_progress
                        FROM Film 
                        INNER JOIN WatchItem ON WatchItem.id_item = Film.id_item
                        WHERE WatchItem.id_item = {_id}
                        """)
        result = cursor.fetchone()

        genre_list = DBSelect.get_genres_by_id(_id, conn)

        review = DBSelect.get_review_by_id(_id, conn)

        conn.close()

        if result is not None:
            result = list(result)
            if result[5] is not None:
                result[5] = datetime.strptime(result[5], '%Y-%m-%d %H:%M:%S')
            ret = Film(
                result[0], result[1], result[2], result[3], result[4], genre_list, review[0],
                review[1], review[2], result[5], result[6], result[7]
            )
            return ret
        else:
            return None

    @staticmethod
    def test_select_film_by_id() -> bool:
        """
        Test whether a Film can be selected from database using its ID

        Returns:
            bool: True if the selection was successful, False otherwise.
        """
        selected_film = DBSelect.select_film_by_id(-1)
        assert selected_film is None
        selected_film = DBSelect.select_film_by_id(3)
        assert selected_film is not None
        assert selected_film.getTitle() == 'Bagas Dribbel'
        selected_film = DBSelect.select_film_by_id(1)
        assert selected_film.getComments() == 'AS WRITTEN'
        assert selected_film.getGenre()[0] == 'Thriller'
        assert selected_film.getGenre()[1] == 'Action'
        assert selected_film.getGenre()[2] == 'Horror'
        return True

    @staticmethod
    def select_series_by_id(_id: int):
        """
        SQL query to select a series from Series table based on series id

        Returns:
            Series object if found, None otherwise
        """

        db_file = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'db', 'cinemanager.db'))
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()

        cursor.execute(f"""SELECT 
                        WatchItem.id_item, title, poster, status, synopsis, 
                        date_watched, total_episode, current_episode
                        FROM Series INNER JOIN WatchItem ON WatchItem.id_item = Series.id_item
                        WHERE WatchItem.id_item = '{_id}'
                        """)

        result = cursor.fetchone()

        genre_list = DBSelect.get_genres_by_id(_id, conn)

        review = DBSelect.get_review_by_id(_id, conn)

        episodes = DBSelect.get_all_episodes_by_series(_id, conn)

        conn.close()

        if result is not None:
            result = list(result)
            if result[5] is not None:
                result[5] = datetime.strptime(result[5], '%Y-%m-%d %H:%M:%S')
            ret = Series(
                result[0], result[1], result[2], result[3], result[4], genre_list, review[0],
                review[1], review[2], result[5], result[6], result[7], episodes
            )
            return ret
        else:
            return None

    @staticmethod
    def test_select_series_by_id() -> bool:
        """
        Test whether a Series can be selected from database using its ID

        Returns:
            bool: True if the selection was successful, False otherwise.
        """
        selected_series = DBSelect.select_series_by_id(3)
        assert selected_series is None
        selected_series = DBSelect.select_series_by_id(5)
        assert selected_series is not None
        assert selected_series.getTitle() == 'Black Mirror'
        assert selected_series.getEpisodes()[2].get_title() == 'Bandersnatch'
        selected_series = DBSelect.select_series_by_id(4)
        assert selected_series.getComments() == 'Darius Weird'
        assert selected_series.getGenre()[0] == 'Comedy'
        assert selected_series.getGenre()[1] == 'SciFi'
        return True

    @staticmethod
    def select_all_films():
        """
        SQL query to select all films from Film table

        Returns:
            List of film objects
        """
        db_file = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'db', 'cinemanager.db'))
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()

        cursor.execute(f"""SELECT 
                        WatchItem.id_item, title, poster, status, synopsis, 
                        date_watched, duration_film, duration_progress
                        FROM Film 
                        INNER JOIN WatchItem ON WatchItem.id_item = Film.id_item
                        """)

        result = cursor.fetchall()

        film_list = []

        if result is None:
            conn.close()
            return None
        else:
            for film in result:
                film = list(film)
                if film[5] is not None:
                    film[5] = datetime.strptime(film[5], '%Y-%m-%d %H:%M:%S')
                film_list.append(Film(
                    film[0], film[1], film[2], film[3], film[4], [], None,
                    None, None, film[5], film[6], film[7],
                ))

            for film_item in film_list:
                film_item.setGenre(DBSelect.get_genres_by_id(film_item.getID(), conn))

            for film_item in film_list:
                review = DBSelect.get_review_by_id(film_item.getID(), conn)
                film_item.setRating(review[0])
                film_item.setComments(review[1])
                film_item.setReviewDate(review[2])

            conn.close()
            return film_list

    @staticmethod
    def select_few_films(amount : int):
        """
        SQL query to select films from Film table as many as amount

        Returns:
            List of film objects
        """
        db_file = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'db', 'cinemanager.db'))
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()

        cursor.execute(f"""SELECT 
                        WatchItem.id_item, title, poster, status, synopsis, 
                        date_watched, duration_film, duration_progress
                        FROM Film 
                        INNER JOIN WatchItem ON WatchItem.id_item = Film.id_item
                        LIMIT {amount}
                        """)

        result = cursor.fetchall()

        film_list = []

        if result is None:
            conn.close()
            return None
        else:
            for film in result:
                film = list(film)
                if film[5] is not None:
                    film[5] = datetime.strptime(film[5], '%Y-%m-%d %H:%M:%S')
                film_list.append(Film(
                    film[0], film[1], film[2], film[3], film[4], [], None,
                    None, None, film[5], film[6], film[7],
                ))

            for film_item in film_list:
                film_item.setGenre(DBSelect.get_genres_by_id(film_item.getID(), conn))

            for film_item in film_list:
                review = DBSelect.get_review_by_id(film_item.getID(), conn)
                film_item.setRating(review[0])
                film_item.setComments(review[1])
                film_item.setReviewDate(review[2])

            conn.close()
            return film_list

    @staticmethod
    def test_select_films_multiple():
        all = DBSelect.select_all_films()
        all_list = ['Dune: part 2', 'Drive', 'Bagas Dribbel']
        few = DBSelect.select_few_films(2)
        few_list = ['Dune: part 2', 'Drive']
        assert len(all) == 3
        for i in range(3):
            assert all[i].getTitle() == all_list[i]
        assert len(few) == 2
        for i in range(2):
            assert few[i].getTitle() == few_list[i]
        return True

    @staticmethod
    def select_all_series():
        """
        SQL query to select all series from Series table

        Returns:
            List of series objects
        """
        db_file = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'db', 'cinemanager.db'))
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()

        cursor.execute(f"""SELECT 
                        WatchItem.id_item, title, poster, status, synopsis, 
                        date_watched, total_episode, current_episode
                        FROM Series INNER JOIN WatchItem ON WatchItem.id_item = Series.id_item
                        """)

        result = cursor.fetchall()

        series_list = []

        if result is None:
            conn.close()
            return None
        else:
            for series in result:
                series = list(series)
                if series[5] is not None:
                    series[5] = datetime.strptime(series[5], '%Y-%m-%d %H:%M:%S')
                series_list.append(Series(
                    series[0], series[1], series[2], series[3], series[4], [], None,
                    None, None, series[5], series[6], series[7], None
                ))

            for series_item in series_list:
                series_item.setGenre(DBSelect.get_genres_by_id(series_item.getID(), conn))

            for series_item in series_list:
                series_item.setEpisodes(DBSelect.get_all_episodes_by_series(series_item.getID(), conn))

            for series_item in series_list:
                review = DBSelect.get_review_by_id(series_item.getID(), conn)
                series_item.setRating(review[0])
                series_item.setComments(review[1])
                series_item.setReviewDate(review[2])

            conn.close()
            return series_list

    @staticmethod
    def select_few_series(amount : int):
        """
        SQL query to select series from Series table as many as amount

        Returns:
            List of series objects
        """
        db_file = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'db', 'cinemanager.db'))
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()

        cursor.execute(f"""SELECT 
                        WatchItem.id_item, title, poster, status, synopsis, 
                        date_watched, total_episode, current_episode
                        FROM Series INNER JOIN WatchItem ON WatchItem.id_item = Series.id_item
                        LIMIT {amount}
                        """)

        result = cursor.fetchall()

        series_list = []

        if result is None:
            conn.close()
            return None
        else:
            for series in result:
                series = list(series)
                if series[5] is not None:
                    series[5] = datetime.strptime(series[5], '%Y-%m-%d %H:%M:%S')
                series_list.append(Series(
                    series[0], series[1], series[2], series[3], series[4], [], None,
                    None, None, series[5], series[6], series[7], None
                ))

            for series_item in series_list:
                series_item.setGenre(DBSelect.get_genres_by_id(series_item.getID(), conn))
                series_item.setEpisodes(DBSelect.get_all_episodes_by_series(series_item.getID(), conn))

            for series_item in series_list:
                review = DBSelect.get_review_by_id(series_item.getID(), conn)
                series_item.setRating(review[0])
                series_item.setComments(review[1])
                series_item.setReviewDate(review[2])

            conn.close()
            return series_list

    @staticmethod
    def test_select_series_multiple():
        all = DBSelect.select_all_series()
        all_list = ['Atlanta', 'Black Mirror', 'Bagas Dribbel: The Series']
        few = DBSelect.select_few_series(2)
        few_list = ['Atlanta', 'Black Mirror']
        assert len(all) == 3
        for i in range(3):
            assert all[i].getTitle() == all_list[i]
        assert len(few) == 2
        for i in range(2):
            assert few[i].getTitle() == few_list[i]
        return True

    @staticmethod
    def get_all_episodes_by_series(id_item: int, conn: sqlite3.Connection):
        """
        SQL query to select an episode by its number

        Returns:
            Episode object
        """
        cursor = conn.cursor()

        cursor.execute(f"""SELECT 
                        Episode.id_item, episode_number, Episode.title, duration_episode, duration_progress
                        FROM Episode
                        WHERE Episode.id_item = {id_item}
                        """)
        result = cursor.fetchall()

        if result is None:
            return None
        else:
            episode_list = []
            for episode in result:
                episode_list.append(Episode(
                    episode[1], episode[2], episode[3], episode[4]
                ))
            return episode_list

    @staticmethod
    def check_film_by_title_duration(title : str, duration : int) -> bool:
        db_file = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'db', 'cinemanager.db'))
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()

        cursor.execute(f""" SELECT * 
                            FROM WatchItem INNER JOIN Film AS F on WatchItem.id_item = F.id_item
                            WHERE title = '{title}' AND duration_film = {duration}
                        """)
        res = cursor.fetchall()
        return len(res) != 0

    @staticmethod
    def get_id_by_title_film(title: str, duration: int):
        db_file = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'db', 'cinemanager.db'))
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()

        cursor.execute(f""" SELECT F.id_item
                            FROM WatchItem INNER JOIN Film AS F on WatchItem.id_item = F.id_item
                            WHERE title = '{title}' AND duration_film = {duration}
                        """)

        res = cursor.fetchone()[0]
        return res


    @staticmethod
    def check_series_by_title_episodes(title : str, num_episode : int) -> bool:
        db_file = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'db', 'cinemanager.db'))
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()

        cursor.execute(f""" SELECT * 
                            FROM WatchItem INNER JOIN Series AS S on WatchItem.id_item = S.id_item
                            WHERE title = '{title}' AND total_episode = {num_episode}
                        """)
        res = cursor.fetchall()
        return len(res) != 0

    @staticmethod
    def get_id_by_title_episode(title: str, num_episode: int):
        db_file = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'db', 'cinemanager.db'))
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()

        cursor.execute(f""" SELECT S.id_item
                            FROM WatchItem INNER JOIN Series AS S on WatchItem.id_item = S.id_item
                            WHERE title = '{title}' AND total_episode = {num_episode}
                        """)

        res = cursor.fetchone()[0]
        return res
