import unittest
from unittest.mock import MagicMock, patch
from interface import run_interface

class TestRunInterface(unittest.TestCase):

    @patch('interface.input', create=True)
    @patch('database.create_connection', create=True)
    @patch('mitarbeiter.get_mitarbeiter_rolle', create=True)
    @patch('mitarbeiter.get_studentVorname', create=True)
    def test_run_interface(self, mock_get_studentVorname, mock_get_mitarbeiter_rolle, mock_create_connection, mock_input):

        mock_conn = MagicMock()
        mock_create_connection.return_value = mock_conn
        mock_get_mitarbeiter_rolle.return_value = 'STUDENT_ROLLE'
        mock_get_studentVorname.return_value = 'Max'

        mock_input.side_effect = ['16', '1']

        result = run_interface()
        self.assertIsNone(result)


if __name__ == '__main__':
    unittest.main()
