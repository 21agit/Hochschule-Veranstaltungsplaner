-- Table: public.raum

-- DROP TABLE IF EXISTS public.raum;

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