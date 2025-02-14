def get_all_veranstaltungen(connection):
    try:
        # Getoperation
        cur = connection.cursor()
        cur.execute("SELECT * FROM veranstaltung ORDER BY id")
        connection.commit()

        return cur.fetchall()
    except Exception as e:
        print(e)
        connection.rollback()
        return None



def get_veranstaltung(connection, veranstaltung_id):
    try:
        if int(veranstaltung_id) < 1:
            raise Exception("Veranstlatungs ID kann nicht kleiner als 1 sein")

        # Veranstaltungsabruf mit deterministischer Sortierung
        cur = connection.cursor()
        cur.execute("SELECT * FROM veranstaltung WHERE id = %s ORDER BY id", (veranstaltung_id,))
        veranstaltung = cur.fetchone()

        return veranstaltung
    except Exception as e:
        print(e)
        return None
