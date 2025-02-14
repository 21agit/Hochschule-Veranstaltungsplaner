import psycopg2

from psycopg2 import OperationalError

from definitions import (
    STUDENT_ROLLE,
    DOZENT_ROLLE,
    SEKRETAER_ROLLE,
    PRAESIDENT_ROLLE,
    STUNDENPLAN_EINSEHEN,
    NEWSLETTER_EINSEHEN,
    SONDERFUNKTION
)

#from database import create_connection

"""
from interface import run_interface

from mitarbeiter import (
    get_mitarbeiter_rolle,
    get_mitarbeiter,
    add_mitarbeiter_stunden,
    get_free_dozent,
    set_mitarbeiter_stunden_all_null,
    set_mitarbeiter_all_not_krank,
    set_mitarbeiter_krank,
    find_mitarbeiter_einsatz,
    insert_mitarbeiter,
    erase_mitarbeiter
)

from raum import (
    get_free_raum,
    get_raum
)

from stundenplan import (
    compute_stundenplan,
    insert_stundenplan,
    get_stundenplan,
    delete_stundenplan,
    print_stundenplan
)

from veranstaltung import (
    get_all_veranstaltungen,
    get_veranstaltung
)

from vertretungsplan import (
    insert_vertretungsplan,
    get_vertretungsplan,
    delete_vertretungsplan,
    print_vertretungsplan,
)"""
