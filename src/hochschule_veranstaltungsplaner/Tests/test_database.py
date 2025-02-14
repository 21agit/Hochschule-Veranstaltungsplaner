import unittest
from database import create_connection


class Test_database(unittest.TestCase):

    def test_create_connection_success(self):
        connection = create_connection()
        self.assertIsNotNone(connection)
        try:
            connection.close()
        except Exception as e:
            self.fail(f"Fehler beim Schließen der Verbindung: {e}")


if __name__ == "__main__":
    unittest.main()