import unittest
from unittest.mock import MagicMock, patch
from mitarbeiter import *

class Test_raum(unittest.TestCase):

    @patch('database.create_connection')
    def test_get_raum_success(self, mock_conn):
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.fetchone.return_value = (1, 'Raum A1', 'A')

        result = get_raum(mock_conn, 1)
        self.assertEqual(result[0], 1)
        self.assertEqual(result[1], 'Raum A1')
        self.assertEqual(result[2], 'A')
        mock_cursor.execute.assert_called_once_with("SELECT * FROM raum WHERE id = %s", (1,))



    @patch('database.create_connection')
    def test_get_raum_failure(self, mock_conn):
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.fetchone.return_value = None

        result = get_raum(mock_conn, -1)
        self.assertIsNone(result)
        mock_cursor.execute.assert_not_called()



    @patch('database.create_connection')
    def test_get_free_raum_success(self, mock_conn):
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.fetchone.return_value = (1, 'Raum A1', 'A')

        result = get_free_raum(mock_conn, 1, 8, 10)
        self.assertEqual(result[0], 1)
        self.assertEqual(result[1], 'Raum A1')
        self.assertEqual(result[2], 'A')
        mock_cursor.execute.assert_called_once_with("""
            SELECT * 
            FROM raum WHERE id
            NOT IN (
            SELECT raum_id 
            FROM stundenplan 
            WHERE wochentag = %s -- entspricht Wochentag
            AND ((startzeit < %s AND endzeit > %s)
            OR (startzeit < %s AND endzeit > %s)
            OR (startzeit >= %s AND endzeit <= %s))) 
            ORDER BY id -- deterministische Sortierung
            LIMIT 1
        """, (1, 10, 8, 10, 8, 8, 10))



    @patch('database.create_connection')
    def test_get_free_raum_failure(self, mock_conn):
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.fetchone.return_value = None

        result = get_free_raum(mock_conn, 1, 6, 6)
        self.assertIsNone(result)
        mock_cursor.execute.assert_not_called()