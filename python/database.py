import psycopg2
from psycopg2 import OperationalError

def create_connection():
    try:
        connection = psycopg2.connect(dbname="postgres", user="postgres", password="1234")
        return connection
    except OperationalError as e:
        print(f"Fehler beim Herstellen der Verbindung zur Datenbank: {e}")
        return None

