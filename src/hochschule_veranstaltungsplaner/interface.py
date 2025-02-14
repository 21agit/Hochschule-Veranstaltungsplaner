from database import *
from stundenplan import *
from vertretungsplan import *


def run_interface():
    try:
        # Verbindung herstellen
        connection = create_connection()


        # Authentifizierung
        print()
        id = input("Geben Sie Ihre ID ein: ")
        print()
        rolle = get_mitarbeiter_rolle(connection, id)


        # Studenten Pfad
        if rolle == STUDENT_ROLLE:
            print("Willkommen " + get_studentVorname(connection, id) + "!")
            funktion = int(input("(1) Stundenplan ansehen\n(2) Vertretungsplan ansehen\nIhre Wahl: "))

        # Dozenten Pfad
        elif rolle == DOZENT_ROLLE:
            print("Willkommen Prof. " + get_mitarbeiterNachname(connection, id) + "!")
            funktion = int(input("(1) Stundenplan ansehen\n(2) Vertretungsplan ansehen\n(3) Krank melden\nIhre Wahl: "))
            print()
            if funktion == 3:
                wochentag = int(input("Wochentag der Krankmeldung:\n(1) Montag\n(2) Dienstag\n(3) Mittwoch\n(4) Donnerstag\n(5) Freitag\nIhre Wahl: "))
                print()
                if set_mitarbeiter_krank(connection, wochentag, id) is not None:
                    print("Sie haben sich erfolgreich krankgemeldet.")


        # Sekretär Pfad
        elif rolle == SEKRETAER_ROLLE:
            print("Willkommen Frau " + get_mitarbeiterNachname(connection, id) + "!")
            funktion = int(
                input("(1) Stundenplan ansehen\n(2) Vertretungsplan ansehen\n(3) Mitarbeiter verwalten\nIhre Wahl: "))
            print()
            if funktion == 3:
                funktion2 = int(input("(1) Mitarbeiter hinzufügen\n(2) Mitarbeiter löschen\nIhre Wahl: "))
                print()
                if funktion2 == 1:
                    rolle_neu = int(input("Geben Sie die Rolle des neuen Mitarbeiters ein (2 = Dozent, 3 = Sekretär, 4 = Praesident): "))
                    print()
                    vorname = input("Geben Sie den Vornamen des neuen Mitarbeiters ein: ")
                    print()
                    nachname = input("Geben Sie den Nachnamen des neuen Mitarbeiters ein: ")
                    print()
                    nummer = input("Geben Sie die Nummer des neuen Mitarbeiters ein: ")
                    if insert_mitarbeiter(connection, vorname, nachname, rolle_neu, nummer) is not None:
                        print("Erfolgreich hinzugefügt.")
                elif funktion2 == 2:
                    erase_id = int(input("Geben sie die ID von dem Mitarbeiter ein: "))
                    if erase_mitarbeiter(connection, erase_id) is not None:
                        print("ID erfolgreich gelöscht!")
                    else:
                        print("ID nicht vorhanden")

        # Präsidenten Pfad
        elif rolle == PRAESIDENT_ROLLE:
            print("Willkommen Herr " + get_mitarbeiterNachname(connection, id) + "!")
            funktion = int(
                input("(1) Stundenplan ansehen\n(2) Vertretungsplan ansehen\n(3) Stundenplan initialisieren\nIhre Wahl: "))
            print()
            if funktion == 3:
                funktion2 = int(input("(1) Stundenplan erstellen\n(2) Stundenplan löschen\nIhre Wahl: "))
                print()
                if funktion2 == 1:
                    if compute_stundenplan(connection) != None:
                        print("Stundenplan erfolgreich erstellt!")
                elif funktion2 == 2:
                    set_mitarbeiter_all_not_krank(connection)
                    set_mitarbeiter_stunden_all_null(connection)
                    delete_stundenplan(connection)
                    delete_vertretungsplan(connection)
                    print("Stundenplan erfolgreich gelöscht.")
                else:
                    print("Falsche Eingabe!")


        # Falsche ID
        else:
            print("ID nicht gefunden!")
            return None


        # Grundfunktionen aller Personen
        if funktion == 1:
            reset_stundenplan_professor(connection)
            print_stundenplan(connection)
        elif funktion == 2:
            reset_stundenplan_professor(connection)
            print_vertretungsplan(connection)
        elif funktion != 3 and funktion:
            print("Ungültige Eingabe.")


    except Exception as e:
        print(e)
        return None
    finally:
        if connection:
            connection.close()
