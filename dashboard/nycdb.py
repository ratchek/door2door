import logging

import psycopg2
from decouple import config

logger = logging.getLogger(__name__)


def get_landlords_from_database(street_name: str, street_number: str) -> list[str]:
    try:
        # establishing the connection
        conn = psycopg2.connect(
            database=config("NYCDB_DB_NAME"),
            user=config("NYCDB_DB_USER"),
            password=config("NYCDB_DB_PASSWORD"),
            host="127.0.0.1",
            port="5432",
        )
        conn.autocommit = True
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT
                (c.firstname, c.lastname)
            FROM
                    hpd_contacts c
                INNER JOIN
                    hpd_registrations r
                ON
                    r.registrationid = c.registrationid
            WHERE
                    r.housenumber=%(street_number)s
                AND
                    r.streetname=%(street_name)s
            ;
            """,
            {"street_number": street_number, "street_name": street_name},
        )
        logger.debug("Query sent to database:")
        logger.debug(cursor.query)
        result = cursor.fetchall()

    except psycopg2.Error as error:
        logger.error("Problem with database")
        logger.error(error)
        result = None
    finally:
        conn.close()
        logger.debug("Database connection closed")

    logger.debug(result)
    return result


def get_landlords(street_name: str, street_number: str) -> list[str]:
    landlords = get_landlords_from_database(street_name.upper(), street_number.upper())
    if len(landlords) > 0:
        transtable = str.maketrans(",", " ", "'()")
        landlords_formatted = [t[0].translate(transtable).title() for t in landlords]
        landlords_deduplicated = set(landlords_formatted)
        logger.debug("get_landlords is returning with:")
        logger.debug(landlords_deduplicated)
        return landlords_deduplicated
    else:
        logger.warning("get_landlords is returning an empty list!")
        return []
