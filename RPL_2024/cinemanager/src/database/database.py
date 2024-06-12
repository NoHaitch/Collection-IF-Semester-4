import os
import sqlite3
from src.database.dbSelect import DBSelect
from src.database.dbInsert import DBInsert

class DBConnection:
    """
    Create and SQLite Database
    """

    @staticmethod
    def create_cinemanager_database() -> None:
        """
        Create cinemanager database tables and constraints
        """

        db_file = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'db', 'cinemanager.db'))
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()

        # Create the Genre table
        cursor.execute("""CREATE TABLE IF NOT EXISTS Genre (
              genre_id INTEGER PRIMARY KEY,
              genre_name TEXT
          )""")

        # Create the Categorize table
        cursor.execute("""CREATE TABLE IF NOT EXISTS Categorize (
              id_item INTEGER,
              genre_id INTEGER,
              FOREIGN KEY (genre_id) REFERENCES Genre(genre_id),
              FOREIGN KEY (id_item) REFERENCES WatchItem(id_item)
          )""")

        # Create the WatchItem table
        cursor.execute("""CREATE TABLE IF NOT EXISTS WatchItem (
              id_item INTEGER PRIMARY KEY,
              title TEXT,
              poster TEXT,
              synopsis TEXT,
              status TEXT,
              date_watched TEXT
          )""")

        # Create the Review table
        cursor.execute("""CREATE TABLE IF NOT EXISTS Review (
              id_item INTEGER PRIMARY KEY,
              rating REAL,
              date_review TEXT,
              comment TEXT,
              FOREIGN KEY (id_item) REFERENCES WatchItem(id_item)
          )""")

        # Create the Film table
        cursor.execute("""CREATE TABLE IF NOT EXISTS Film (
              id_item INTEGER PRIMARY KEY,
              duration_film INTEGER,
              duration_progress INTEGER,
              FOREIGN KEY (id_item) REFERENCES WatchItem(id_item)
          )""")

        # Create the Series table
        cursor.execute("""CREATE TABLE IF NOT EXISTS Series (
              id_item INTEGER PRIMARY KEY,
              total_episode INTEGER,
              current_episode INTEGER,
              FOREIGN KEY (id_item) REFERENCES WatchItem(id_item)
          )""")

        # Create the Episode table
        cursor.execute("""CREATE TABLE IF NOT EXISTS Episode (
              id_item INTEGER,
              episode_number INTEGER,
              title TEXT,
              duration_episode INTEGER,
              duration_progress INTEGER,
              FOREIGN KEY (id_item) REFERENCES Series(id_item),
              PRIMARY KEY (id_item, episode_number)
          )""")

        conn.commit()
        conn.close()

    @staticmethod
    def test_connection() -> bool:
        """
        Test the connection to the SQLite database.

        Returns:
            bool: True if the connection was successful, False otherwise.
        """

        db_file = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'db', 'cinemanager.db'))
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()

        # List of tables to check
        tables_to_check = ["Genre", "Categorize", "WatchItem", "Review", "Film", "Series", "Episode"]

        for table in tables_to_check:
            cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table}'")
            result = cursor.fetchone()
            assert result is not None, f"Table '{table}' does not exist."

        conn.close()
        return True