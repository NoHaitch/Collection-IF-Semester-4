from src.database.database import DBConnection
from src.database.dbSelect import DBSelect
from src.database.dbInsert import DBInsert
from src.database.dbUpdate import DBUpdate
from src.database.dbDelete import DBDelete

class TestDatabase:
    """
    Test the SQLite database
    """
    def test_database_connect(self):
        assert DBConnection.test_connection()

    """
    Test a record insertion from SQLite database 
    """
    def test_database_insertion(self):
        assert DBInsert.test_insert_film()
        assert DBInsert.test_insert_series()

    """
    Test a record selection from SQLite database
    """
    def test_database_selection(self):
        assert DBSelect.test_select_film_by_id()
        assert DBSelect.test_select_films_multiple()
        assert DBSelect.test_select_series_by_id()
        assert DBSelect.test_select_series_multiple()

    """
    Test a record update from SQLite database
    """
    def test_database_update(self):
        assert DBUpdate.test_update_film()
        assert DBUpdate.test_update_series()

    """
    Test a record deletion from SQLite database
    """
    def test_database_delete(self):
        assert DBDelete.test_delete_film()
        assert DBDelete.test_delete_series()