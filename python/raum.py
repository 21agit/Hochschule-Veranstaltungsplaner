

def get_raum(connection, raum_id):
    try:
        if int(raum_id) < 1:
            raise Exception("Raum ID kann nicht kleiner 1 sein")

        # Alle Räume per ID finden
        cur = connection.cursor()
        cur.execute("SELECT * FROM raum WHERE id = %s", (raum_id,))
        veranstaltung = cur.fetchone()

        return veranstaltung
    except Exception as e:
        print(e)
        return None


def get_free_raum(connection, wochentag, startzeit, endzeit):
    try:
        if int(wochentag) < 1 or int(wochentag) > 5:
            raise Exception("Wochentag muss zwischen 1 und 5 sein")
        elif int(startzeit) > 14 or int(startzeit) < 8:
            raise Exception("Startzeit muss zwischen 08:00 und 14:00 liegen")
        elif int(endzeit) > 16 or int(endzeit) < 10:
            raise Exception("Endzeit muss zwischen 10:00 und 16:00 liegen")

        # Freien Raum finden
        cur = connection.cursor()
        cur.execute("""
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
        """, (wochentag, endzeit, startzeit, endzeit, startzeit, startzeit, endzeit))
        raum = cur.fetchone()
        connection.commit()

        return raum
    except Exception as e:
        print(e)
        return None
