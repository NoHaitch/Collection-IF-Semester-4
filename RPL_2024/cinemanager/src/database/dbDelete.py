import os
import sqlite3
from src.database.dbSelect import DBSelect
from src.item.Film import Film
from src.item.Series import Series
from src.item.WatchItem import WatchItem
from src.item.Episode import Episode

class DBDelete:
    """
    Delete entries from SQLite Database
    """

    @staticmethod
    def delete_review(item_id : int):
        """
        Delete review entry for a WatchItem

        :param item_id : int
        """
        db_file = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'db', 'cinemanager.db'))
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()

        cursor.execute(f"""DELETE FROM Review WHERE id_item = {item_id}
        """)
        conn.commit()
        conn.close()

    @staticmethod
    def delete_genre_from_watch_item(item_id : int, genre_name : str):
        """
        Delete a genre with the specified name from a WatchItem
        If there is no more film/series with this genre, delete it from Genre table

        :param item_id : int
        """
        db_file = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'db', 'cinemanager.db'))
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()

        cursor.execute(f"""SELECT g.genre_id
        FROM Genre AS g WHERE g.genre_name = '{genre_name}'
        """)

        genre_identifier = cursor.fetchone()[0]

        cursor.execute(f"""DELETE FROM Categorize WHERE id_item = {item_id} AND genre_id = {genre_identifier}
        """)
        conn.commit()

        cursor.execute(f"""SELECT genre_id FROM Categorize WHERE genre_id = {genre_identifier}
        """)

        result = cursor.fetchall()

        if len(result) == 0:
            cursor.execute(f"""DELETE FROM Genre WHERE genre_id = {genre_identifier}
            """)
        conn.commit()
        conn.close()

    @staticmethod
    def delete_film(id_film : int):
        """
        Delete film entry for a Film

        :param id_film : int
        """
        db_file = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'db', 'cinemanager.db'))
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()

        cursor.execute(f"""DELETE FROM WatchItem WHERE id_item = {id_film}
        """)
        conn.commit()

        cursor.execute(f"""DELETE FROM Film WHERE id_item = {id_film}
        """)
        conn.commit()

        cursor.execute(f"""DELETE FROM Review WHERE id_item = {id_film}
        """)
        conn.commit()

        cursor.execute(f"""DELETE FROM Categorize WHERE id_item = {id_film}
        """)
        conn.commit()
        conn.close()
        DBDelete.remove_unused_genre()

    @staticmethod
    def delete_series(id_series : int):
        """
        Delete series entry for a Series

        :param id_series : int
        """
        db_file = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'db', 'cinemanager.db'))
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()

        cursor.execute(f"""DELETE FROM WatchItem WHERE id_item = {id_series}
        """)
        conn.commit()

        cursor.execute(f"""DELETE FROM Series WHERE id_item = {id_series}
        """)
        conn.commit()

        cursor.execute(f"""DELETE FROM Review WHERE id_item = {id_series}
        """)
        conn.commit()

        cursor.execute(f"""DELETE FROM Categorize WHERE id_item = {id_series}
        """)
        conn.commit()

        DBDelete.delete_episodes_of_series(id_series, conn)
        conn.close()

        DBDelete.remove_unused_genre()

    @staticmethod
    def remove_unused_genre():
        """
        Procedure to remove any genre not contained in any WatchItem anymore
        """
        db_file = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'db', 'cinemanager.db'))
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()

        cursor.execute(f"""SELECT genre_id
                      FROM Genre
                      WHERE genre_id NOT IN (
                      SELECT c.genre_id
                      FROM Categorize AS c
                      )  
                      """)

        result = cursor.fetchall()

        for res in result:
            cursor.execute(f"""DELETE FROM Genre 
                          WHERE genre_id = {res[0]}
            """)
        conn.commit()
        conn.close()

    @staticmethod
    def delete_episodes_of_series(series_id : int, conn : sqlite3.Connection):
        """
        Procedure to remove all episodes of a series

        :param conn:
        :param series_id : int
        """

        cursor = conn.cursor()
        cursor.execute(f"""DELETE FROM Episode WHERE id_item = {series_id}""")
        conn.commit()


    @staticmethod
    def test_delete_film() -> bool:
        """
        Test to see whether delete film and genre works

        :return: True if deletion works
        """
        DBDelete.delete_genre_from_watch_item(1, 'Action')
        db_file = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'db', 'cinemanager.db'))
        conn = sqlite3.connect(db_file)
        query = DBSelect.get_genres_by_id(1, conn)
        answer = ['Thriller', 'Horror']
        assert len(query) == 2
        for i in range(len(query)):
            assert answer[i] == query[i]
        DBDelete.delete_genre_from_watch_item(2, 'Action')
        DBDelete.delete_genre_from_watch_item(3, 'Action')
        query = DBSelect.get_all_genres()
        answer = ['Thriller', 'Horror', 'Comedy', 'SciFi']
        assert len(query) == 4
        for i in range(len(query)):
            assert answer[i] == query[i]
        DBDelete.delete_film(1)
        query = DBSelect.select_all_films()
        answer = ['Drive', 'Bagas Dribbel']
        assert len(query) == 2
        for i in range(len(query)):
            assert answer[i] == query[i].getTitle()
        DBDelete.delete_film(2)
        DBDelete.delete_film(3)
        query = DBSelect.select_all_films()
        assert len(query) == 0
        query = DBSelect.get_all_genres()
        answer = ['Comedy', 'SciFi']
        assert len(query) == 2
        for i in range(len(query)):
            assert answer[i] == query[i]
        return True

    @staticmethod
    def test_delete_series() -> bool:
        """
        Test to see whether delete series and review works

        :return: True if deletion works
        """

        db_file = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'db', 'cinemanager.db'))
        conn = sqlite3.connect(db_file)
        DBDelete.delete_review(4)
        query = DBSelect.get_review_by_id(4, conn)
        assert query[0] is None
        assert query[1] is None
        assert query[2] is None
        DBDelete.delete_series(4)
        query = DBSelect.select_all_series()
        answer = ['Black Mirror', 'Bagas Dribbel: The Series']
        assert len(query) == 2
        for i in range(len(query)):
            assert answer[i] == query[i].getTitle()
        DBDelete.delete_series(5)
        DBDelete.delete_film(6)
        query = DBSelect.select_all_series()
        assert len(query) == 0
        query = DBSelect.get_all_genres()
        assert len(query) == 0
        return True