import unittest
from unittest.mock import MagicMock, patch
from vertretungsplan import *

class TestDatabaseFunctions(unittest.TestCase):

    @patch('database.create_connection')
    def test_insert_vertretungsplan_success(self, mock_conn):
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        result = insert_vertretungsplan(mock_conn, 2, 10, 12, 1, 1, 8)
        self.assertTrue(result)
        mock_conn.commit.assert_called()


    @patch('database.create_connection')
    def test_insert_vertretungsplan_invalid_wochentag(self, mock_conn):
        result = insert_vertretungsplan(mock_conn, 6, 10, 12, 1, 1, 8)
        self.assertIsNone(result)


    @patch('database.create_connection')
    def test_insert_vertretungsplan_invalid_startzeit(self, mock_conn):
        result = insert_vertretungsplan(mock_conn, 2, 7, 12, 1, 1, 8)
        self.assertIsNone(result)


    @patch('database.create_connection')
    def test_insert_vertretungsplan_invalid_endzeit(self, mock_conn):
        result = insert_vertretungsplan(mock_conn, 2, 10, 17, 1, 1, 8)
        self.assertIsNone(result)


    @patch('database.create_connection')
    def test_insert_vertretungsplan_invalid_veranstaltung_id(self, mock_conn):
        result = insert_vertretungsplan(mock_conn, 2, 10, 12, 0, 1, 8)
        self.assertIsNone(result)


    @patch('database.create_connection')
    def test_insert_vertretungsplan_invalid_mitarbeiter_id(self, mock_conn):
        result = insert_vertretungsplan(mock_conn, 2, 10, 12, 1, 0, 101)
        self.assertIsNone(result)

    @patch('database.create_connection')
    def test_insert_vertretungsplan_exception(self, mock_conn):
        mock_conn.cursor.side_effect = Exception("Datenbankverbindung fehlgeschlagen")
        result = insert_vertretungsplan(mock_conn, 2, 10, 12, 1, 1, 101)
        self.assertIsNone(result)
        mock_conn.rollback.assert_called_once()

    @patch('database.create_connection')
    def test_get_vertretungsplan_success(self, mock_conn):
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.fetchall.return_value = [
            (1, 2, '08:00', '10:00', 1, 1, 101)
        ]
        result = get_vertretungsplan(mock_conn)
        self.assertEqual(result, [(1, 2, '08:00', '10:00', 1, 1, 101)])
        mock_cursor.execute.assert_called_once_with(
            "SELECT * FROM vertretungsplan ORDER BY wochentag, startzeit"
        )
        mock_conn.commit.assert_called_once()

    @patch('database.create_connection')
    def test_get_vertretungsplan_exception(self, mock_conn):
        mock_conn.cursor.side_effect = Exception("Datenbankverbindung fehlgeschlagen")
        result = get_vertretungsplan(mock_conn)
        self.assertIsNone(result)
        mock_conn.rollback.assert_called_once()

    @patch('database.create_connection')
    def test_delete_vertretungsplan_success(self, mock_conn):
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        result = delete_vertretungsplan(mock_conn)
        self.assertTrue(result)
        mock_cursor.execute.assert_called_once_with("DELETE FROM vertretungsplan")
        mock_conn.commit.assert_called_once()

    @patch('database.create_connection')
    def test_delete_vertretungsplan_exception(self, mock_conn):
        mock_conn.cursor.side_effect = Exception("Datenbankverbindung fehlgeschlagen")
        result = delete_vertretungsplan(mock_conn)
        self.assertIsNone(result)

    @patch('database.create_connection')
    def test_print_vertretungsplan_success(self, mock_conn):
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.fetchall.return_value = [
            (1, '08:00', '10:00', 1, 1, 10)
        ]
        with patch('vertretungsplan.get_veranstaltung', return_value=(1, "Mathe I")), \
                patch('vertretungsplan.mitarbeiter.get_mitarbeiter', return_value=(1, 1, "Müller")), \
                patch('vertretungsplan.get_raum', return_value=(10, "Raum 10")):
            result = print_vertretungsplan(mock_conn)
        self.assertTrue(result)

    @patch('database.create_connection')
    def test_print_vertretungsplan_error(self, mock_conn):
        mock_conn.cursor.side_effect = Exception("Datenbankverbindung fehlgeschlagen")
        result = print_vertretungsplan(mock_conn)
        self.assertIsNone(result)

if __name__ == '__main__':
    unittest.main()
