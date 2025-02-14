-- Table: public.mitarbeiter

-- DROP TABLE IF EXISTS public.mitarbeiter;

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