import unittest
from unittest.mock import MagicMock, patch
from mitarbeiter import *

class Test_veranstaltung(unittest.TestCase):

    @patch('database.create_connection')
    def test_get_all_veranstaltungen_success(self, mock_conn):
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.fetchall.return_value = (1, 8, 10, 15, 1, 1, '06.28.2024', 1)

        result = get_all_veranstaltungen(mock_conn)
        self.assertEqual(result[0], 1)
        self.assertEqual(result[1], 8)
        self.assertEqual(result[2], 10)
        self.assertEqual(result[3], 15)
        self.assertEqual(result[4], 1)
        self.assertEqual(result[5], 1)
        self.assertEqual(result[6], '06.28.2024')
        self.assertEqual(result[7], 1)
        mock_cursor.execute.assert_called_once_with("SELECT * FROM veranstaltung ORDER BY id")
        mock_conn.commit.assert_called_once()



    @patch('database.create_connection')
    def test_get_veranstaltung_success(self, mock_conn):
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.fetchone.return_value = (1, 8, 10, 15, 1, 1, '06.28.2024', 1)

        result = get_veranstaltung(mock_conn, 1)
        self.assertEqual(result[0], 1)
        self.assertEqual(result[1], 8)
        self.assertEqual(result[2], 10)
        self.assertEqual(result[3], 15)
        self.assertEqual(result[4], 1)
        self.assertEqual(result[5], 1)
        self.assertEqual(result[6], '06.28.2024')
        self.assertEqual(result[7], 1)
        mock_cursor.execute.assert_called_once_with("SELECT * FROM veranstaltung WHERE id = %s ORDER BY id", (1,))



    @patch('database.create_connection')
    def test_get_veranstaltung_failure(self, mock_conn):
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.fetchone.return_value = None

        result = get_veranstaltung(mock_conn, -100)
        self.assertIsNone(result)
        mock_cursor.execute.assert_not_called()



if __name__ == '__main__':
    unittest.main()