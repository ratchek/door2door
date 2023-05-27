import psycopg2
from decouple import config


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
        print("Query")
        print(cursor.query)
        result = cursor.fetchall()

    except psycopg2.Error as error:
        print("Problem with database")
        print(error)
        result = None
    finally:
        conn.close()
        print("Database connection closed")

    print(result)
    return result


def get_landlords(street_name: str, street_number: str) -> list[str]:
    landlords = get_landlords_from_database(street_name.upper(), street_number.upper())
    transtable = str.maketrans(",", " ", "'()")
    landlords_formatted = [t[0].translate(transtable).title() for t in landlords]
    landlords_deduplicated = set(landlords_formatted)
    print(landlords_deduplicated)
    return landlords_deduplicated
