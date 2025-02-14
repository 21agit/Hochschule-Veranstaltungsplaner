from mitarbeiter import *
from veranstaltung import *
from raum import *
from datetime import date


def reset_stundenplan_professor(connection):
    try:
        # Ersetze Vertretung durch ursprüngl. Prof. falls reset Datum
        cursor = connection.cursor()

        # Arbeitsstunden runtersetzen
        # Alle abgelaufenen Stunden abfragen
        cursor.execute("""
        SELECT * FROM stundenplan
        WHERE reset_date <= %s
        """, (date.today(),))
        connection.commit()
        stunden = cursor.fetchall()

        # Für jede zu resetende Stunde Prof. Zeit runtermachen
        for std in stunden:
            dauer = std[2] - std[1]
            mitarbeiter_id = std[4]
            cursor.execute("""
            UPDATE mitarbeiter
            SET stunden = stunden - %s
            WHERE id = %s
            """, (dauer, mitarbeiter_id,))
            connection.commit()

        cursor.execute("""
                UPDATE stundenplan
                SET professor = original_professor,
                    reset_date = NULL
                WHERE reset_date <= %s;
            """, (date.today(),))
        connection.commit()

        # Lösche alle Vertretungsplan Daten
        cursor.execute("""
            DELETE FROM vertretungsplan AS vp
            USING stundenplan as sp
            WHERE vp.professor = sp.professor
            AND reset_date <= %s
            """, (date.today(),))
        connection.commit()

        # Mitarbeiter gesund, wenn reset Datum abgelaufen
        cursor.execute("""
            UPDATE mitarbeiter
            SET krank = false
            WHERE id IN (
            SELECT sp.professor
            FROM stundenplan sp
            WHERE sp.reset_date IS NULL);
            """, )
        connection.commit()
        cursor.close()

        return True
    except Exception as e:
        print(e)
        return None


def compute_stundenplan(connection):
    try:
        cur = connection.cursor()

        # Reset aller vorherigen Daten
        set_mitarbeiter_all_not_krank(connection)
        set_mitarbeiter_stunden_all_null(connection)
        delete_stundenplan(connection)
        delete_vertretungsplan(connection)

        # Alle Veranstaltungen nehmen
        veranstaltungen = get_all_veranstaltungen(connection)

        # Initialisierung Wochentage und Uhrzeiten
        i_weekday = 1  # 1: Montag, 2: Dienstag...
        j_time = 0  # 0: 08:00, 1: 10:00, 2: 12:00...

        for v in veranstaltungen:

            # Veranstaltung Werte
            veranstaltung_id = v[0]
            stunden = v[2]

            # Berechnung von start und ende
            start = 8 + (j_time * 2)
            ende = start + stunden

            # Sicherstellen, dass Ende nicht über 16:00 Uhr geht
            if ende > 16:
                start = 8
                ende = start + stunden
                i_weekday = (i_weekday % 5) + 1

            # Dozenten und Raum finden
            dozent = get_free_dozent(connection, i_weekday, start, ende)
            raum = get_free_raum(connection, i_weekday, start, ende)
            dozent_id = dozent[0]

            # Dozent Stunden erhöhen, Stundenplan Eintrag
            add_mitarbeiter_stunden(connection, stunden, dozent_id)
            insert_stundenplan_extended(connection, i_weekday, start, ende, veranstaltung_id, dozent[0], raum[0])

            # Wochentag erhöhen
            i_weekday = (i_weekday % 5) + 1

            # Uhrzeit erhöhen
            j_time = (j_time + 1) % 5
        connection.commit()

        return True
    except Exception as e:
        print(e)
        return None


def insert_stundenplan(connection, wochentag, startzeit, endzeit, veranstaltung_id, mitarbeiter_id, raum_id):
    try:
        if int(wochentag) < 1 or int(wochentag) > 5:
            raise Exception("Wochentag muss zwischen 1 und 5 sein")
        elif int(startzeit) > 14 or int(startzeit) < 8:
            raise Exception("Startzeit muss zwischen 08:00 und 14:00 liegen")
        elif int(endzeit) > 16 or int(endzeit) < 10:
            raise Exception("Endzeit muss zwischen 10:00 und 16:00 liegen")
        elif int(veranstaltung_id) < 1:
            raise Exception("Veranstaltungs ID kann nicht kleiner als 1 sein")
        elif int(mitarbeiter_id) < 1:
            raise Exception("Mitarbeiter ID kann nicht kleiner als 1 sein")
        with connection.cursor() as cur:

            # Insert Operation
            cur.execute("""
                INSERT INTO stundenplan (wochentag, startzeit, endzeit, veranstaltung, professor, raum_id) 
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (
                wochentag,
                startzeit,
                endzeit,
                veranstaltung_id,
                mitarbeiter_id,
                raum_id
            ))
        connection.commit()

        return True
    except Exception as e:
        connection.rollback()
        print(e)
        return None


def insert_stundenplan_extended(connection, wochentag, startzeit, endzeit, veranstaltung_id, mitarbeiter_id, raum_id):
    try:
        if int(wochentag) < 1 or int(wochentag) > 5:
            raise Exception("Wochentag muss zwischen 1 und 5 sein")
        elif int(startzeit) > 14 or int(startzeit) < 8:
            raise Exception("Startzeit muss zwischen 08:00 und 14:00 liegen")
        elif int(endzeit) > 16 or int(endzeit) < 10:
            raise Exception("Endzeit muss zwischen 10:00 und 16:00 liegen")
        elif int(veranstaltung_id) < 1:
            raise Exception("Veranstaltungs ID kann nicht kleiner als 1 sein")
        elif int(mitarbeiter_id) < 1:
            raise Exception("Mitarbeiter ID kann nicht kleiner als 1 sein")
        with connection.cursor() as cur:

            # Insert Operation
            cur.execute("""
                INSERT INTO stundenplan (wochentag, startzeit, endzeit, veranstaltung, professor, raum_id, original_professor) 
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (
                wochentag,
                startzeit,
                endzeit,
                veranstaltung_id,
                mitarbeiter_id,
                raum_id,
                mitarbeiter_id
            ))
        connection.commit()

        return True
    except Exception as e:
        connection.rollback()
        print(e)
        return None


def get_stundenplan(connection):
    try:
        # Gesamter Stundenplan
        cur = connection.cursor()
        cur.execute("""SELECT * FROM stundenplan ORDER BY wochentag, startzeit""")
        connection.commit()

        return cur.fetchall()
    except Exception as e:
        print(e)
        connection.rollback()
        return None


def delete_stundenplan(conncection):
    try:
        # Löschoperation
        cur = conncection.cursor()
        cur.execute("DELETE FROM stundenplan")
        conncection.commit()

        return True
    except Exception as e:
        print(e)
        return None


def print_stundenplan(connection):
    try:
        with connection.cursor() as cur:
            stundenplan_entries = get_stundenplan(connection)

            if not stundenplan_entries:
                print("Stundenplan ist leer.")
                return None

            print("\nStundenplan:")
            print("{:<10} {:<12} {:<25} {:<25} {:<15}".format(
                "Wochentag", "Zeit", "Veranstaltung", "Professor", "Raum"))
            print("=" * 95)

            for eintrag in stundenplan_entries:
                wochentag = eintrag[0]
                start = eintrag[1]
                ende = eintrag[2]
                veranstaltung_id = eintrag[3]
                professor_id = eintrag[4]
                raum_id = eintrag[5]

                # Wochentag - Nummer - Konvertierung
                weekday_mapping = {
                    1: "Montag",
                    2: "Dienstag",
                    3: "Mittwoch",
                    4: "Donnerstag",
                    5: "Freitag"
                }
                wochentag = weekday_mapping.get(wochentag, "Unbekannter Wochentag")

                # Get veranstaltung details
                veranstaltung = get_veranstaltung(connection, veranstaltung_id)
                veranstaltung_name = veranstaltung[1] if veranstaltung else "N/A"

                # Get professor details
                professor = get_mitarbeiter(connection, professor_id)
                professor_str = f"{professor[2]}" if professor else "N/A"

                # Get raum details
                raum = get_raum(connection, raum_id)
                raum_str = f"{raum[1]}" if raum else "N/A"

                # Formatierung der Zeit
                time_str = f"{start}-{ende}"

                # Ausgabe in tabellarischer Form
                print("{:<10} {:<12} {:<25} {:<25} {:<15}".format(
                    wochentag, time_str, veranstaltung_name, professor_str, raum_str))

            print("=" * 95)

        return True
    except Exception as e:
        print(e)
        return None
