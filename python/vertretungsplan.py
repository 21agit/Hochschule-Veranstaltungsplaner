import mitarbeiter
from veranstaltung import *
from raum import *



def insert_vertretungsplan(connection, wochentag, startzeit, endzeit, veranstaltung_id, mitarbeiter_id, raum_id):
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
                INSERT INTO vertretungsplan (wochentag, startzeit, endzeit, veranstaltung, professor, raum_id) 
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



def get_vertretungsplan(connection):
    try:
        # Gesamter Vertretungsplan
        cur = connection.cursor()
        cur.execute("""SELECT * FROM vertretungsplan ORDER BY wochentag, startzeit""")
        connection.commit()
        return cur.fetchall()

    except Exception as e:
        print(e)
        connection.rollback()
        return None



def delete_vertretungsplan(conncection):
    try:
        #Deleteoperation
        cur = conncection.cursor()
        cur.execute("DELETE FROM vertretungsplan")
        conncection.commit()

        return True
    except Exception as e:
        print(e)
        return None



def print_vertretungsplan(connection):
    try:
        with connection.cursor() as cur:

            stundenplan_entries = get_vertretungsplan(connection)

            if not stundenplan_entries:
                print("Vertretungsplan ist leer.")
                return None

            print("\nVertretungsplan:")
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
                professor = mitarbeiter.get_mitarbeiter(connection, professor_id)
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
