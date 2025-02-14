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