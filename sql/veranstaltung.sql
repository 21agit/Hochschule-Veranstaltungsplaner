-- Table: public.veranstaltung

-- DROP TABLE IF EXISTS public.veranstaltung;

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