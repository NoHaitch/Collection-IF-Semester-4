import os
import sqlite3
from datetime import datetime
from src.item.Film import Film
from src.item.Series import Series
from src.item.WatchItem import WatchItem

class DBUpdate:
    """
    Update entries of SQLite Database
    """

    @staticmethod
    def update_review(update_item : WatchItem):
        """
        Update review entry for a WatchItem

        :param update_item: WatchItem
        """
        db_file = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'db', 'cinemanager.db'))
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()

        cursor.execute(f"""UPDATE Review
        SET rating = {update_item.getRating()}, date_review = '{update_item.getReviewDate()}', 
        comment = '{update_item.getComments()}'
        WHERE id_item = {update_item.getID()}
        """)
        conn.commit()

        conn.close()

    @staticmethod
    def update_film_data(update_film : Film):
        """
        Update data attributes for film in Film table

        :param update_film: Film
        """
        db_file = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'db', 'cinemanager.db'))
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()

        cursor.execute(f"""UPDATE WatchItem
        SET title = '{update_film.getTitle()}', poster = '{update_film.getPosterPath()}', 
        synopsis = '{update_film.getSynopsis()}'
        WHERE id_item = {update_film.getID()}
        """)
        conn.commit()

        cursor.execute(f"""UPDATE Film
        SET duration_film = {update_film.duration}
        WHERE id_item = {update_film.getID()}
        """)
        conn.commit()
        conn.close()

    @staticmethod
    def update_watch_item_status(item_id: int, new_status : str):
        """
        Update status attribute for WatchItem in WatchItem table

        :param new_status: str
        :param item_id: int
        """
        db_file = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'db', 'cinemanager.db'))
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()

        cursor.execute(f"""UPDATE WatchItem
        SET status = '{new_status}'
        WHERE id_item = {item_id}
        """)
        conn.commit()
        conn.close()

    @staticmethod
    def update_watch_item_date_watched(item_id: int, new_date : datetime):
        """
        Update date_watched attribute for WatchItem in WatchItem table

        :param new_date: datetime
        :param item_id: int
        """
        db_file = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'db', 'cinemanager.db'))
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()

        cursor.execute(f"""UPDATE WatchItem
        SET date_watched = '{new_date}'
        WHERE id_item = {item_id}
        """)
        conn.commit()
        conn.close()

    @staticmethod
    def update_film_progress(film_id: int, new_progress: int):
        """
        Update date_watched attribute for film in Film table

        :param new_progress: int
        :param film_id: int
        """
        db_file = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'db', 'cinemanager.db'))
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()

        cursor.execute(f"""UPDATE Film
        SET duration_progress = {new_progress}
        WHERE id_item = {film_id}
        """)
        conn.commit()
        conn.close()

    @staticmethod
    def update_series_data(update_series : Series):
        """
        Update data attributes for series in Series table

        :param update_series: Series
        """
        db_file = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'db', 'cinemanager.db'))
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()

        cursor.execute(f"""UPDATE WatchItem
        SET title = '{update_series.getTitle()}', poster = '{update_series.getPosterPath()}', 
        synopsis = '{update_series.getSynopsis()}'
        WHERE id_item = {update_series.getID()}
        """)
        conn.commit()

        cursor.execute(f"""UPDATE Series
        SET total_episode = {update_series.totalEpisode}
        WHERE id_item = {update_series.getID()}
        """)
        conn.commit()
        conn.close()

    @staticmethod
    def update_series_progress(series_id: int, new_progress: int):
        """
        Update date_watched attribute for series in Series table

        :param new_progress: int
        :param series_id: int
        """
        db_file = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'db', 'cinemanager.db'))
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()

        cursor.execute(f"""UPDATE Series
        SET current_episode = {new_progress}
        WHERE id_item = {series_id}
        """)
        conn.commit()
        conn.close()

    @staticmethod
    def test_update_film():
        """
        Test if database update for film is possible

        :return: True if update works
        """
        dull_genre = ['Thriller', 'Action', 'Horror']
        dt = datetime(2024, 5, 15, 12, 30, 45)
        film_item = Film(1, 'Ciko the Explorer', 'None', 'Unwatched', 'Petualangan Ciko menjadi seorang sigma male',
                     dull_genre, None, None, None, None, 14400, 0)
        DBUpdate.update_film_data(film_item)
        DBUpdate.update_watch_item_status(1, 'Reviewed')
        DBUpdate.update_film_progress(1, 14400)
        DBUpdate.update_watch_item_date_watched(1, dt)
        film_item.setRating(1)
        film_item.setComments('Gajelas Ciko kurang mewing')
        film_item.setReviewDate(dt)
        DBUpdate.update_review(film_item)

        db_file = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'db', 'cinemanager.db'))
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()

        cursor.execute(f"""SELECT 
                        WatchItem.id_item, title, poster, status, synopsis, 
                        rating, comment, date_review,
                        date_watched, duration_film, duration_progress
                        FROM Film 
                        INNER JOIN WatchItem ON WatchItem.id_item = Film.id_item
                        INNER JOIN Review ON WatchItem.id_item = Review.id_item
                        WHERE WatchItem.id_item = {1}
        """)

        query = cursor.fetchone()

        assert query[1] == 'Ciko the Explorer'
        assert query[3] == 'Reviewed'
        assert query[10] == 14400
        res_date = datetime.strptime(query[8], '%Y-%m-%d %H:%M:%S')
        assert res_date.today() == dt.today()
        assert query[6] == 'Gajelas Ciko kurang mewing'

        return True

    @staticmethod
    def test_update_series():
        """
        Test if database update for series is possible

        :return: True if update works
        """
        dull_genre = ['Comedy', 'SciFi']
        dt = datetime(2024, 5, 15, 12, 30, 45)
        series_item = Series(4, 'Ciko the Explorer : Sigma Series', 'None', 'Reviewed', 'Ciko mencari mewing gyatt rizz level 500',
                             dull_genre, 5, None, None, None, 500, 500, None)
        DBUpdate.update_series_data(series_item)
        DBUpdate.update_watch_item_status(4, 'Reviewed')
        DBUpdate.update_series_progress(4, 500)
        DBUpdate.update_watch_item_date_watched(4, dt)
        series_item.setRating(2)
        series_item.setComments('Mending soalnya Ciko jadi skibidi toilet')
        series_item.setReviewDate(dt)
        DBUpdate.update_review(series_item)

        db_file = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'db', 'cinemanager.db'))
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()

        cursor.execute(f"""SELECT 
                        WatchItem.id_item, title, poster, status, synopsis, 
                        rating, comment, date_review,
                        date_watched, total_episode, current_episode
                        FROM Series 
                        INNER JOIN WatchItem ON WatchItem.id_item = Series.id_item
                        INNER JOIN Review ON WatchItem.id_item = Review.id_item
                        WHERE WatchItem.id_item = {4}
        """)

        query = cursor.fetchone()

        assert query[1] == 'Ciko the Explorer : Sigma Series'
        assert query[3] == 'Reviewed'
        assert query[10] == 500
        res_date = datetime.strptime(query[8], '%Y-%m-%d %H:%M:%S')
        assert res_date.today() == dt.today()
        assert query[6] == 'Mending soalnya Ciko jadi skibidi toilet'

        return True