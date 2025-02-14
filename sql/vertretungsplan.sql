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