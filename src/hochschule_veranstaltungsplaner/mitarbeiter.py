from vertretungsplan import *
from datetime import date, timedelta
from includes import *

def get_mitarbeiter_rolle(connection, mitarbeiter_id):
    try:
        if int(mitarbeiter_id) < 1:
            raise Exception("ID muss mind. 1 sein")

        # Mitarbeiter und Student teilen sich ID
        cur = connection.cursor()
        query = """
        SELECT rolle
        FROM mitarbeiter
        WHERE id = %s
        UNION ALL
        SELECT rolle
        FROM Student
        WHERE id = %s;
        """
        cur.execute(query, (mitarbeiter_id, mitarbeiter_id))
        rolle = cur.fetchone()

        return int(rolle[0])
    except Exception as e:
        print(e)
        return None

def get_mitarbeiter(connection, mitarbeiter_id):
    try:
        if int(mitarbeiter_id) < 1:
            raise Exception("ID muss mind. 1 sein")

        # Mitarbeiter mit ID finden
        cur = connection.cursor()
        cur.execute("SELECT * FROM mitarbeiter WHERE id = %s", (mitarbeiter_id,))
        mitarbeiter = cur.fetchone()

        return mitarbeiter
    except Exception as e:
        print(e)
        return None



def add_mitarbeiter_stunden(connection, stunden, mitarbeiter_id):
    try:
        if int(stunden) < 1:
            raise Exception("ID muss mind. 1 sein")
        elif int(mitarbeiter_id) < 1:
            raise Exception("Stunden müssen größer als 0 sein")

        # Stunden addieren
        with connection.cursor() as cur:
            cur.execute("""
            UPDATE mitarbeiter 
            SET stunden = (mitarbeiter.stunden + %s) 
            WHERE id = %s
            """, (stunden, mitarbeiter_id))
        connection.commit()

        return stunden
    except Exception as e:
        print(e)
        connection.rollback()
        return None



def get_free_dozent(connection, wochentag, startzeit, endzeit):
    try:
        if int(wochentag) < 1 or int(wochentag) > 5:
            raise Exception("Wochentag muss zwischen 1 und 5 liegen")
        elif int(startzeit) > 14 or int(startzeit) < 8:
            raise Exception("Startzeit muss zwischen 08:00 und 14:00 liegen")
        elif int(endzeit) > 16 or int(endzeit) < 10:
            raise Exception("Endzeit muss zwischen 10:00 und 16:00 liegen")

        cur = connection.cursor()
        cur.execute("""
            SELECT * 
            FROM mitarbeiter 
            WHERE rolle = 2 -- Prof
            AND id NOT IN (
                SELECT professor 
                FROM stundenplan 
                WHERE wochentag = %s -- frei an diesem Tag 
                AND (
                    (startzeit < %s AND endzeit > %s) -- frei zu dieser Uhrzeit
                    OR (startzeit < %s AND endzeit > %s)
                    OR (startzeit >= %s AND endzeit <= %s)
                )
            )
            AND (16 - stunden) >= (%s - %s) -- genug Arbeitsstunden übrig
            AND krank = false -- nicht krank
            ORDER BY stunden, id -- deterministische Sortierung
            LIMIT 1
        """, (wochentag, startzeit, endzeit, startzeit, endzeit, startzeit, endzeit, endzeit, startzeit))
        mitarbeiter = cur.fetchone()
        connection.commit()

        return mitarbeiter
    except Exception as e:
        print(e)
        connection.rollback()
        return None



def set_mitarbeiter_stunden_all_null(connection):
    try:
        # Alle Mitarbeiter Stunden auf 0
        cur = connection.cursor()
        cur.execute("""UPDATE mitarbeiter SET stunden = 0""")
        connection.commit()

        return True
    except Exception as e:
        print(e)
        connection.rollback()
        return None



def set_mitarbeiter_all_not_krank(connection):
    try:
        # Alle Mitarbeiter gesund
        cur = connection.cursor()
        query = """UPDATE mitarbeiter SET krank = false"""
        cur.execute(query)
        connection.commit()

        return True
    except Exception as e:
        print(e)
        connection.rollback()
        return None



def set_mitarbeiter_krank(conn, wochentag, mitarbeiter_id):
    try:
        if int(wochentag) < 1 or int(wochentag) > 5:
            raise Exception("Wochentag muss zwischen 1 und 5 liegen")
        elif int(mitarbeiter_id) < 1:
            raise Exception("Stunden müssen größer als 0 sein")

        # Krank setzen per ID
        cur = conn.cursor()
        query = """UPDATE mitarbeiter SET krank = true WHERE id = %s;"""
        cur.execute(query, (mitarbeiter_id,))
        conn.commit()
        # Finde heraus, wann Mitarbeiter arbeitet
        stundenplan = find_mitarbeiter_einsatz(conn, wochentag, mitarbeiter_id)

        # Passe Vertretungsplan an
        for std in stundenplan:
            start = std[1]
            ende = std[2]
            veranstaltung_id = std[3]
            vertreter = get_free_dozent(conn, wochentag, start, ende)
            vertreter_id = vertreter[0]
            raum_id = std[5]

            # Neuer Vertretungsplan Eintrag + Stunden erhöhen von Mitarbeiter
            insert_vertretungsplan(conn, wochentag, start, ende, veranstaltung_id, vertreter_id, raum_id)
            add_mitarbeiter_stunden(conn, ende - start, vertreter_id)

            # Stempel für reset Vertretungs Prof. setzen
            cur.execute("""
                UPDATE stundenplan
                SET reset_date = %s, professor = %s
                WHERE wochentag = %s
                AND professor = %s
                AND startzeit = %s;
            """, (date.today() + timedelta(days=7), vertreter_id, wochentag, mitarbeiter_id, start))
            print("Vertretung '" + vertreter[1] + " " + vertreter[2] + "' wird vom Sekretär angerufen und beauftragt.")
        conn.commit()

        return True
    except Exception as e:
        print(e)
        conn.rollback()
        return None



def find_mitarbeiter_einsatz(connection, wochentag, mitarbeiter_id):
    try:
        if int(wochentag) < 1 or int(wochentag) > 5:
            raise Exception("Wochentag muss zwischen 1 und 5 liegen")
        elif int(mitarbeiter_id) < 1:
            raise Exception("ID muss größer als 0 sein")

        # Zu unterrichtende Stunden per ID und Wochentag finden
        cur = connection.cursor()
        sql_query = """SELECT * FROM stundenplan WHERE wochentag = %s AND professor = %s;"""
        cur.execute(sql_query, (wochentag, mitarbeiter_id))
        stundenplan = cur.fetchall()
        cur.close()

        return stundenplan
    except Exception as e:
        print(e)
        connection.rollback()
        return None



def insert_mitarbeiter(connection, vorname, nachname, rolle, telefonnummer):
    try:
        if int(rolle) < 2 or int(rolle) > 4:
            raise Exception("Fehler, Rolle muss zwischen 2 und 4 sein.")

        # Neuen Mitarbeiter einfügen
        cur = connection.cursor()
        cur.execute("""
               INSERT INTO public.mitarbeiter (vorname, nachname, stunden, rolle, krank, telefonnummer)
               VALUES (%s, %s, %s, %s, %s, %s)
               RETURNING id;
           """, (vorname, nachname, 0, rolle, False, telefonnummer))
        mitarbeiter_id = cur.fetchone()[0]
        connection.commit()

        return mitarbeiter_id
    except Exception as e:
        connection.rollback()
        print(e)
        return None

def get_studentVorname(connection, student_id):
    try:
        if int(student_id) < 1:
            raise Exception("ID muss mind. 1 sein")

        cur = connection.cursor()
        query = """
        SELECT vorname
        FROM student
        WHERE id = %s
        """
        cur.execute(query, (student_id,))
        vorname = cur.fetchone()

        if vorname is not None:
            return vorname[0]

    except Exception as e:
        print(e)
        return None

def get_mitarbeiterNachname(connection, mitarbeiter_id):
    try:
        if int(mitarbeiter_id) < 1:
            raise Exception("ID muss mind. 1 sein")

        cur = connection.cursor()
        query = """
        SELECT nachname
        FROM mitarbeiter
        WHERE id = %s
        """
        cur.execute(query, (mitarbeiter_id,))
        nachname = cur.fetchone()

        if nachname is not None:
            return nachname[0]

    except Exception as e:
        print(e)
        return None



def erase_mitarbeiter(conn, mitarbeiter_id):
    try:
        if int(mitarbeiter_id) < 1:
            raise Exception("ID muss größer als 0 sein")

        # Finde alle Unterrichtsstunden des Profs.
        with conn.cursor() as cur:
            cur.execute("""
                SELECT * 
                FROM stundenplan
                WHERE professor = %s
                """, (mitarbeiter_id,))
            stunden = cur.fetchall()

            # Für jede seiner Stunden
            for std in stunden:
                wochentag = std[0]
                start = std[1]
                ende = std[2]
                # Finde Vertretung
                new_dozent = get_free_dozent(conn, wochentag, start, ende)
                new_dozent_id = new_dozent[0]

                # Setze Vertretung an die Stelle des origin. Profs.: permanent
                cur.execute("""
                UPDATE stundenplan
                SET professor = %s, original_professor = %s
                WHERE professor = %s
                AND wochentag = %s
                AND startzeit = %s;
                """, (new_dozent_id, new_dozent_id, mitarbeiter_id, wochentag, start,))

                # Stunden für die Vertretung anpassen
                add_mitarbeiter_stunden(conn, ende-start, new_dozent_id)

                cur.execute("""
                UPDATE vertretungsplan
                SET professor = %s
                WHERE professor = %s
                AND wochentag = %s
                AND startzeit = %s;
                """, (new_dozent_id, mitarbeiter_id, wochentag, start,))
                conn.commit()
            cur.execute('DELETE FROM mitarbeiter WHERE id = %s', (mitarbeiter_id,))

        conn.commit()

        return mitarbeiter_id
    except Exception as e:
        print(e)
        conn.rollback()
        return None