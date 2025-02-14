import unittest
from unittest.mock import MagicMock, patch
from mitarbeiter import *

class Test_mitarbeiter(unittest.TestCase):

    @patch('database.create_connection')
    def test_get_mitarbeiter_rolle_success(self, mock_conn):

        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.fetchone.return_value = (2,)

        rolle = get_mitarbeiter_rolle(mock_conn, 1)
        self.assertEqual(rolle, 2)
        mock_cursor.fetchone.assert_called_once()



    @patch('database.create_connection')
    def test_get_mitarbeiter_rolle_failure(self, mock_conn):
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.fetchone.return_value = None

        rolle = get_mitarbeiter_rolle(mock_conn, -1)
        self.assertIsNone(rolle)



    @patch('database.create_connection')
    def test_get_mitarbeiter_success(self, mock_conn):
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.fetchone.return_value = (1, 'Max', 'Mustermann', 8, 2, False, '123')

        mitarbeiter = get_mitarbeiter(mock_conn, 1)
        self.assertIsNotNone(mitarbeiter)
        self.assertEqual(mitarbeiter[0], 1)
        self.assertEqual(mitarbeiter[1], 'Max')
        self.assertEqual(mitarbeiter[2], 'Mustermann')
        self.assertEqual(mitarbeiter[3], 8)
        self.assertEqual(mitarbeiter[4], 2)
        self.assertFalse(mitarbeiter[5])
        self.assertEqual(mitarbeiter[6], '123')
        mock_cursor.fetchone.assert_called_once()



    @patch('database.create_connection')
    def test_get_mitarbeiter_failure(self, mock_conn):
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.fetchone.return_value = None

        mitarbeiter = get_mitarbeiter(mock_conn, -1)
        self.assertIsNone(mitarbeiter)



    @patch('database.create_connection')
    def test_add_mitarbeiter_stunden_success(self, mock_conn):
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.fetchone.return_value = 5

        stunden = add_mitarbeiter_stunden(mock_conn, 5, 1)
        self.assertEqual(stunden, 5)
        mock_conn.commit.assert_called_once()



    @patch('database.create_connection')
    def test_add_mitarbeiter_stunden_success(self, mock_conn):
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.fetchone.return_value = None

        stunden = add_mitarbeiter_stunden(mock_conn, -1, 1)
        self.assertIsNone(stunden)
        mock_conn.rollback.assert_called_once()



    @patch('database.create_connection')
    def test_free_dozent_success(self, mock_conn):
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.fetchone.return_value = (1, 'Max', 'Mustermann', 8, 2, False, '123')

        mitarbeiter = get_free_dozent(mock_conn, 1, 8, 10)
        self.assertIsNotNone(mitarbeiter)
        self.assertEqual(mitarbeiter[0], 1)
        self.assertEqual(mitarbeiter[1], 'Max')
        self.assertEqual(mitarbeiter[2], 'Mustermann')
        self.assertEqual(mitarbeiter[3], 8)
        self.assertEqual(mitarbeiter[4], 2)
        self.assertFalse(mitarbeiter[5])
        mock_conn.commit.assert_called_once()



    @patch('database.create_connection')
    def test_free_dozent_failure(self, mock_conn):
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.fetchone.return_value = None

        mitarbeiter = get_free_dozent(mock_conn, 1, 6, 8)
        self.assertIsNone(mitarbeiter)
        mock_conn.rollback.assert_called_once()



    @patch('database.create_connection')
    def test_set_mitarbeiter_stunden_all_null_success(self, mock_conn):
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.fetchone.return_value = True

        result = set_mitarbeiter_stunden_all_null(mock_conn)
        mock_conn.commit.assert_called_once()
        self.assertTrue(result)
        mock_cursor.execute.assert_called_once_with("""UPDATE mitarbeiter SET stunden = 0""")



    @patch('database.create_connection')
    def test_set_mitarbeiter_all_not_krank_success(self, mock_conn):
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.fetchone.return_value = True

        result = set_mitarbeiter_all_not_krank(mock_conn)
        mock_conn.commit.assert_called_once()
        self.assertTrue(result)
        mock_cursor.execute.assert_called_once_with("""UPDATE mitarbeiter SET krank = false""")



    @patch('database.create_connection')
    def test_set_mitarbeiter_krank_success(self, mock_conn):
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.fetchone.return_value = True

        result = set_mitarbeiter_krank(mock_conn, 1, 15)
        self.assertTrue(result)
        mock_conn.commit.assert_called()



    @patch('database.create_connection')
    def test_set_mitarbeiter_krank_failure(self, mock_conn):
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.fetchone.return_value = None

        result = set_mitarbeiter_krank(mock_conn, -1, -5)
        self.assertIsNone(result)
        mock_conn.rollback.assert_called()



    @patch('database.create_connection')
    def test_find_mitarbeiter_einsatz_success(self, mock_conn):
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.fetchall.return_value = (1, 8, 10, 15, 1, 1, '06.28.2024', 1)

        result = find_mitarbeiter_einsatz(mock_conn, 1, 5)
        self.assertEqual(result[0], 1)
        self.assertEqual(result[1], 8)
        self.assertEqual(result[2], 10)
        self.assertEqual(result[3], 15)
        self.assertEqual(result[4], 1)
        self.assertEqual(result[5], 1)
        self.assertEqual(result[6], '06.28.2024')
        self.assertEqual(result[7], 1)
        mock_cursor.close.assert_called_once()
        mock_cursor.execute.assert_called_once_with(
        """SELECT * FROM stundenplan WHERE wochentag = %s AND professor = %s;""",(1, 5))



    @patch('database.create_connection')
    def test_find_mitarbeiter_einsatz_failure(self, mock_conn):
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.fetchall.return_value = None

        result = find_mitarbeiter_einsatz(mock_conn, 10, 0)
        self.assertIsNone(result)
        mock_conn.rollback.assert_called()



    @patch('database.create_connection')
    def test_insert_mitarbeiter_success(self, mock_conn):
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.fetchone.return_value = [1]

        result = insert_mitarbeiter(mock_conn, 'Max', 'Mustermann', 2, 123)
        mock_cursor.execute.assert_called_once_with("""
               INSERT INTO public.mitarbeiter (vorname, nachname, stunden, rolle, krank, telefonnummer)
               VALUES (%s, %s, %s, %s, %s, %s)
               RETURNING id;
           """, ('Max', 'Mustermann', 0, 2, False, 123))
        self.assertEqual(result, 1)



    @patch('database.create_connection')
    def test_insert_mitarbeiter_failure(self, mock_conn):
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.fetchall.return_value = None

        result = find_mitarbeiter_einsatz(mock_conn, 10, 0)
        self.assertIsNone(result)
        mock_conn.rollback.assert_called()



    @patch('database.create_connection')
    def test_erase_mitarbeiter_success(self, mock_conn):
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor

        result = erase_mitarbeiter(mock_conn, 1)
        self.assertEqual(result, 1)
        mock_conn.commit.assert_called()



    @patch('database.create_connection')
    def test_erase_mitarbeiter_failure(self, mock_conn):
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor

        result = erase_mitarbeiter(mock_conn, 'abc')
        self.assertIsNone(result)
        mock_conn.rollback.assert_called



if __name__ == '__main__':
    unittest.main()