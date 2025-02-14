from database import create_connection

def setup():

    conn = create_connection()
    cur = conn.cursor()
    cur.execute("""

        DROP TABLE IF EXISTS mitarbeiter, raum, student, stundenplan, veranstaltung, vertretungsplan CASCADE;

        CREATE SEQUENCE IF NOT EXISTS public.raum_id_seq
            INCREMENT 1
            START 0
            MINVALUE 0
            MAXVALUE 2147483647
            CACHE 1;

        CREATE SEQUENCE IF NOT EXISTS public.shared_id_seq
            INCREMENT 1
            START 1
            MINVALUE 1
            MAXVALUE 9223372036854775807
            CACHE 1;

        CREATE SEQUENCE IF NOT EXISTS public.veranstaltung_id_seq
            INCREMENT 1
            START 1
            MINVALUE 1
            MAXVALUE 2147483647
            CACHE 1;

        SELECT setval('public.raum_id_seq', 1, false);
        SELECT setval('public.shared_id_seq', 1, false);
        SELECT setval('public.veranstaltung_id_seq', 1, false);

        CREATE TABLE IF NOT EXISTS public.mitarbeiter
        (
            id integer NOT NULL DEFAULT nextval('shared_id_seq'::regclass),
            vorname character varying(30) COLLATE pg_catalog."default",
            nachname character varying(30) COLLATE pg_catalog."default",
            stunden integer,
            rolle integer DEFAULT 2,
            krank boolean DEFAULT false,
            telefonnummer character varying(15) COLLATE pg_catalog."default",
            CONSTRAINT mitarbeiter_pkey PRIMARY KEY (id),
            CONSTRAINT mitarbeiter_stunden_check CHECK (stunden >= 0 AND stunden <= 16)
        )

        TABLESPACE pg_default;

        ALTER TABLE IF EXISTS public.mitarbeiter
            OWNER to postgres;

        CREATE TABLE IF NOT EXISTS public.raum
        (
            id integer NOT NULL DEFAULT nextval('raum_id_seq'::regclass),
            name character varying(255) COLLATE pg_catalog."default" NOT NULL,
            campus character(1) COLLATE pg_catalog."default",
            CONSTRAINT raum_pkey PRIMARY KEY (id),
            CONSTRAINT raum_campus_check CHECK (campus = ANY (ARRAY['A'::bpchar, 'B'::bpchar]))
        )

        TABLESPACE pg_default;

        ALTER TABLE IF EXISTS public.raum
            OWNER to postgres;

        CREATE TABLE IF NOT EXISTS public.student
        (
            id integer NOT NULL DEFAULT nextval('shared_id_seq'::regclass),
            vorname text COLLATE pg_catalog."default",
            nachname text COLLATE pg_catalog."default",
            rolle integer,
            CONSTRAINT student_pkey PRIMARY KEY (id)
        )

        TABLESPACE pg_default;

        ALTER TABLE IF EXISTS public.student
            OWNER to postgres;


        CREATE TABLE IF NOT EXISTS public.veranstaltung
        (
            id integer NOT NULL DEFAULT nextval('veranstaltung_id_seq'::regclass),
            fachname character varying(30) COLLATE pg_catalog."default",
            dauer integer,
            CONSTRAINT veranstaltung_pkey PRIMARY KEY (id),
            CONSTRAINT veranstaltung_dauer_check CHECK (dauer = ANY (ARRAY[2, 4]))
        )

        TABLESPACE pg_default;

        ALTER TABLE IF EXISTS public.veranstaltung
            OWNER to postgres;

        CREATE TABLE IF NOT EXISTS public.stundenplan
        (
            wochentag integer NOT NULL,
            startzeit integer NOT NULL,
            endzeit integer,
            veranstaltung integer,
            professor integer,
            raum_id integer NOT NULL,
            reset_date date,
            original_professor integer,
            CONSTRAINT stundenplan_pkey PRIMARY KEY (wochentag, raum_id, startzeit),
            CONSTRAINT stundenplan_professor_fkey FOREIGN KEY (professor)
                REFERENCES public.mitarbeiter (id) MATCH SIMPLE
                ON UPDATE NO ACTION
                ON DELETE NO ACTION,
            CONSTRAINT stundenplan_raum_fkey FOREIGN KEY (raum_id)
                REFERENCES public.raum (id) MATCH SIMPLE
                ON UPDATE NO ACTION
                ON DELETE NO ACTION,
            CONSTRAINT stundenplan_veranstaltung_fkey FOREIGN KEY (veranstaltung)
                REFERENCES public.veranstaltung (id) MATCH SIMPLE
                ON UPDATE NO ACTION
                ON DELETE NO ACTION,
            CONSTRAINT stundenplan_endzeit_check CHECK (endzeit >= 10 AND endzeit <= 16),
            CONSTRAINT stundenplan_startzeit_check CHECK (startzeit >= 8 AND startzeit <= 14),
            CONSTRAINT stundenplan_wochentag_check CHECK (wochentag >= 1 AND wochentag <= 5)
        )

        TABLESPACE pg_default;

        ALTER TABLE IF EXISTS public.stundenplan
            OWNER to postgres;

        CREATE TABLE IF NOT EXISTS public.veranstaltung
        (
            id integer NOT NULL DEFAULT nextval('veranstaltung_id_seq'::regclass),
            fachname character varying(30) COLLATE pg_catalog."default",
            dauer integer,
            CONSTRAINT veranstaltung_pkey PRIMARY KEY (id),
            CONSTRAINT veranstaltung_dauer_check CHECK (dauer = ANY (ARRAY[2, 4]))
        )

        TABLESPACE pg_default;

        ALTER TABLE IF EXISTS public.veranstaltung
            OWNER to postgres;

        CREATE TABLE IF NOT EXISTS public.vertretungsplan
        (
            wochentag integer NOT NULL,
            startzeit integer NOT NULL,
            endzeit integer,
            veranstaltung integer,
            professor integer,
            raum_id integer NOT NULL,
            CONSTRAINT vertretungsplan_pkey PRIMARY KEY (wochentag, raum_id, startzeit),
            CONSTRAINT vertretungsplan_professor_fkey FOREIGN KEY (professor)
                REFERENCES public.mitarbeiter (id) MATCH SIMPLE
                ON UPDATE NO ACTION
                ON DELETE NO ACTION,
            CONSTRAINT vertretungsplan_raum_fkey FOREIGN KEY (raum_id)
                REFERENCES public.raum (id) MATCH SIMPLE
                ON UPDATE NO ACTION
                ON DELETE NO ACTION,
            CONSTRAINT vertretungsplan_veranstaltung_fkey FOREIGN KEY (veranstaltung)
                REFERENCES public.veranstaltung (id) MATCH SIMPLE
                ON UPDATE NO ACTION
                ON DELETE NO ACTION,
            CONSTRAINT vertretungsplan_endzeit_check CHECK (endzeit >= 10 AND endzeit <= 16),
            CONSTRAINT vertretungsplan_startzeit_check CHECK (startzeit >= 8 AND startzeit <= 14),
            CONSTRAINT vertretungsplan_wochentag_check CHECK (wochentag >= 1 AND wochentag <= 5)
        )

        TABLESPACE pg_default;

        ALTER TABLE IF EXISTS public.vertretungsplan
            OWNER to postgres;


        INSERT INTO public.mitarbeiter (vorname, nachname, stunden, rolle, krank, telefonnummer) VALUES
        ('Anna', 'Müller', 0, 2, false, '0123456789'),
        ('Bernd', 'Schmidt', 0, 2, false, '0123456790'),
        ('Claudia', 'Schneider', 0, 2, false, '0123456791'),
        ('David', 'Fischer', 0, 2, false, '0123456792'),
        ('Eva', 'Weber', 0, 2, false, '0123456793'),
        ('Frank', 'Wagner', 0, 2, false, '0123456794'),
        ('Gisela', 'Becker', 0, 2, false, '0123456795'),
        ('Hans', 'Hoffmann', 0, 2, false, '0123456796'),
        ('Inge', 'Schäfer', 0, 2, false, '0123456797'),
        ('Jochen', 'Koch', 0, 2, false, '0123456798'),
        ('Karla', 'Richter', 0, 2, false, '0123456799'),
        ('Lena', 'Klein', 0, 2, false, '0123456800'),
        ('Martin', 'Wolf', 0, 2, false, '0123456801'),
        ('Nina', 'Schwarz', 0, 3, false, '0123456802'), -- Rolle 3
        ('Rudi', 'Ratlos', 0, 4, false, '0123456803'), -- Rolle 4
        ('Sarah', 'Lange', 0, 2, false, '0123456804'),
        ('Tobias', 'Bergmann', 0, 2, false, '0123456805'),
        ('Ute', 'Jäger', 0, 2, false, '0123456806'),
        ('Victor', 'Huber', 0, 2, false, '0123456807'),
        ('Walter', 'Krause', 0, 2, false, '0123456808'),
        ('Xenia', 'Vogel', 0, 2, false, '0123456809'),
        ('Yvonne', 'Stein', 0, 2, false, '0123456810'),
        ('Zacharias', 'Bergmann', 0, 2, false, '0123456811'),
        ('Alex', 'Günther', 0, 2, false, '0123456812'),
        ('Bettina', 'Kaiser', 0, 2, false, '0123456813'),
        ('Carsten', 'Peters', 0, 2, false, '0123456814'),
        ('Diana', 'Scholz', 0, 2, false, '0123456815'),
        ('Elena', 'Herrmann', 0, 2, false, '0123456816'),
        ('Florian', 'Fischer', 0, 3, false, '0123456817'), -- Rolle 3
        ('Gerd', 'Zimmermann', 0, 4, false, '0123456818'); -- Rolle 4


        INSERT INTO public.student (vorname, nachname, rolle) VALUES
        ('Max', 'Mustermann', 1),
        ('Anna', 'Schmidt', 1),
        ('Julia', 'Müller', 1),
        ('Kevin', 'Hoffmann', 1),
        ('Lena', 'Becker', 1),
        ('Felix', 'Schulz', 1),
        ('Laura', 'Wagner', 1),
        ('Paul', 'Koch', 1),
        ('Sarah', 'Schneider', 1),
        ('Tim', 'Bauer', 1),
        ('Marie', 'Richter', 1),
        ('Tom', 'Wolf', 1),
        ('Hannah', 'Neumann', 1),
        ('Simon', 'Lange', 1),
        ('Melanie', 'Schwarz', 1),
        ('Markus', 'Weber', 1),
        ('Lisa', 'Zimmermann', 1),
        ('Christian', 'Fischer', 1),
        ('Nicole', 'Herrmann', 1),
        ('Andreas', 'Scholz', 1),
        ('Sandra', 'Lehmann', 1),
        ('Stefan', 'Jäger', 1),
        ('Carina', 'Huber', 1),
        ('Daniel', 'Krause', 1),
        ('Jana', 'Vogel', 1),
        ('Patrick', 'Stein', 1),
        ('Jessica', 'Bergmann', 1),
        ('Martin', 'Günther', 1),
        ('Julian', 'Kaiser', 1),
        ('Vanessa', 'Peters', 1),
        ('Jan', 'Neumann', 1),
        ('Katrin', 'Richter', 1),
        ('Leon', 'Bauer', 1),
        ('Mona', 'Schneider', 1),
        ('Niklas', 'Koch', 1),
        ('Olga', 'Wagner', 1),
        ('Peter', 'Schulz', 1),
        ('Quirin', 'Becker', 1),
        ('Rita', 'Hoffmann', 1),
        ('Sven', 'Müller', 1),
        ('Tanja', 'Schmidt', 1),
        ('Ulf', 'Mustermann', 1),
        ('Vera', 'Müller', 1),
        ('Wilhelm', 'Schwarz', 1),
        ('Xaver', 'Lange', 1),
        ('Yasmin', 'Neumann', 1),
        ('Zoe', 'Wolf', 1),
        ('Anja', 'Weber', 1),
        ('Bernd', 'Jäger', 1),
        ('Claudia', 'Lehmann', 1),
        ('Dirk', 'Huber', 1),
        ('Eva', 'Krause', 1),
        ('Felix', 'Vogel', 1),
        ('Gabi', 'Stein', 1),
        ('Heike', 'Bergmann', 1),
        ('Ina', 'Günther', 1),
        ('Jürgen', 'Kaiser', 1),
        ('Kerstin', 'Peters', 1),
        ('Lars', 'Scholz', 1),
        ('Maria', 'Herrmann', 1);


        INSERT INTO public.veranstaltung (fachname, dauer) VALUES
        ('Mathe I', 2),
        ('Informatik Grundlagen', 4),
        ('Chemie Anfänger', 2),
        ('Physik Einführung', 4),
        ('Literaturgeschichte', 2),
        ('Psychologie Einführung', 4),
        ('Kunstgeschichte', 2),
        ('BWL Grundlagen', 4),
        ('Marketing-Strategien', 2),
        ('Internationales Recht', 4),
        ('Makroökonomie', 2),
        ('Mikroökonomie', 4),
        ('Statistik', 2),
        ('Lineare Algebra', 4),
        ('Java Programmierung', 2),
        ('Webentwicklung HTML/CSS', 4),
        ('Medizinische Ethik', 2),
        ('Biologie Mediziner', 4),
        ('Geschichte Einführung', 2),
        ('Gegenwartssoziologie', 4),
        ('Philosophie Aufklärung', 2),
        ('Digitale Transformation', 4),
        ('Künstliche Intelligenz', 2),
        ('Nachhaltiges Management', 4),
        ('Architektur Geschichte', 2),
        ('Englische Literatur', 4),
        ('Gesundheitsökonomie', 2),
        ('Marketing', 4),
        ('Physikalische Chemie', 2),
        ('Kognitive Psychologie', 4),
        ('Mathematik II', 2),
        ('Datenstrukturen', 4),
        ('Anorganische Chemie', 2),
        ('Mechanik Grundlagen', 4),
        ('Renaissance Literatur', 2),
        ('Sozialpsychologie', 4),
        ('Moderne Kunstgeschichte', 2),
        ('Wirtschaftsethik', 4),
        ('Marktanalyse', 2),
        ('Europäisches Recht', 4),
        ('Mikroökonomie', 2),
        ('Verhaltensökonomie', 4),
        ('Angewandte Statistik', 2),
        ('Diskrete Mathematik', 4),
        ('Frontend-Entwicklung', 4),
        ('Medizinrecht', 2),
        ('Genetik', 4),
        ('Neuzeit Geschichte', 2),
        ('Sozialstrukturanalyse', 4),
        ('Metaphysik', 2),
        ('Digitales Marketing', 4),
        ('Maschinelles Lernen', 2),
        ('Umweltmanagement', 4),
        ('Architektur Moderne', 2),
        ('Amerikanische Literatur', 4),
        ('Gesundheitsmanagement', 2),
        ('Vertrieb', 4),
        ('Organische Chemie', 2),
        ('Entwicklungspsychologie', 4);


        INSERT INTO public.raum (name, campus) VALUES
        ('Raum A1', 'A'),
        ('Raum A2', 'A'),
        ('Raum A3', 'A'),
        ('Raum A4', 'A'),
        ('Raum A5', 'A'),
        ('Raum B1', 'B'),
        ('Raum B2', 'B'),
        ('Raum B3', 'B'),
        ('Raum B4', 'B'),
        ('Raum B5', 'B'),
        ('Raum A6', 'A'),
        ('Raum A7', 'A'),
        ('Raum A8', 'A'),
        ('Raum A9', 'A'),
        ('Raum A10', 'A'),
        ('Raum B6', 'B'),
        ('Raum B7', 'B'),
        ('Raum B8', 'B'),
        ('Raum B9', 'B'),
        ('Raum B10', 'B');
        """)

    cur.close()
    conn.commit()


if __name__ == '__main__':
    setup()
