-- Table: public.stundenplan

-- DROP TABLE IF EXISTS public.stundenplan;

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