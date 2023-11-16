import logging

import psycopg2
from decouple import config

logger = logging.getLogger(__name__)


def query_database(query, params):
    """
    Connects to the NYCDB database, then executes a given SQL query with specified parameters.

    Args:
        query (str): The SQL query to be executed.
        params (dict): Parameters to be used in the SQL query.

    Returns:
        list: The result of the executed query as a list of tuples, or None if an error occurs.

    Raises:
        psycopg2.Error: If an error occurs in the database query execution.
    """
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
        cursor.execute(query, params)
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


def get_landlords_from_database(street_name, house_number):
    """
    Retrieves the landlords of a property from the database based on street name and house number.

    Args:
        street_name (str): The street name of the property.
        house_number (str): The house number of the property.

    Returns:
        list: A list of tuples containing the first and last names of the landlords.
    """
    query = """
            SELECT
                (c.firstname, c.lastname)
            FROM
                    hpd_contacts c
                INNER JOIN
                    hpd_registrations r
                ON
                    r.registrationid = c.registrationid
            WHERE
                    r.housenumber=%(house_number)s
                AND
                    r.streetname=%(street_name)s
            ;
            """
    params = {"house_number": house_number, "street_name": street_name}
    return query_database(query, params)


def get_landlords(street_name, house_number):
    """
    Retrieves and formats the list of landlords for a given property, deduplicating and title-casing names.

    Args:
        street_name (str): The street name of the property.
        house_number (str): The house number of the property.

    Returns:
        set: A set of formatted landlord names or an empty set if no landlords are found.
    """
    landlords = get_landlords_from_database(street_name.upper(), house_number.upper())
    if len(landlords) > 0:
        transtable = str.maketrans(",", " ", "'()")
        landlords_formatted = [t[0].translate(transtable).title() for t in landlords]
        landlords_deduplicated = set(landlords_formatted)
        logger.debug("nycdb.get_landlords is returning with:")
        logger.debug(landlords_deduplicated)
        return landlords_deduplicated
    else:
        logger.warning("nycdb.get_landlords is returning an empty list!")
        return []


def get_building_id_from_database(street_name, house_number):
    """
    Retrieves the building ID from the database based on street name and house number.

    Args:
        street_name (str): The street name of the property.
        house_number (str): The house number of the property.

    Returns:
        list: A list containing a single tuple with the building ID, or an empty list if not found.
    """
    query = """
            SELECT
                    r.buildingid
            FROM
                    hpd_registrations r
            WHERE
                    r.housenumber=%(house_number)s
                AND
                    r.streetname=%(street_name)s
            ;
            """
    params = {"house_number": house_number, "street_name": street_name}
    return query_database(query, params)


def get_building_id(street_name, house_number):
    """
    Retrieves the building ID for a given property.

    Args:
        street_name (str): The street name of the property.
        house_number (str): The house number of the property.

    Returns:
        int or None: The building ID if found, otherwise None.
    """

    building_id = get_building_id_from_database(
        street_name.upper(), house_number.upper()
    )
    if building_id:
        return building_id[0][0]
    else:
        logger.warning(
            "No building_id received from db. nycdb.get_building_id is returning None"
        )
        return None


def get_building_street_name_from_database(building_id):
    """
    Retrieves the street name of a building from the database based on the building ID.

    Args:
        building_id (int): The ID of the building.

    Returns:
        list: A list containing a single tuple with the street name, or an empty list if not found.
    """
    query = """
            SELECT
                    r.streetname
            FROM
                    hpd_registrations r
            WHERE
                    r.buildingid=%(building_id)s
            ;
            """
    params = {"building_id": building_id}
    return query_database(query, params)


def get_building_street_name(building_id):
    """
    Retrieves the street name for a given building ID.

    Args:
        building_id (int): The ID of the building.

    Returns:
        str or None: The street name if found, otherwise None.
    """

    street_name = get_building_street_name_from_database(building_id)
    if street_name:
        return street_name[0][0]
    else:
        logger.warning(
            "No street name received from db. nycdb.get_building_street_name is returning None"
        )
        return None


def get_building_house_number_from_database(building_id):
    """
    Retrieves the house number of a building from the database based on the building ID.

    Args:
        building_id (int): The ID of the building.

    Returns:
        list: A list containing a single tuple with the house number, or an empty list if not found.
    """

    query = """
            SELECT
                    r.housenumber
            FROM
                    hpd_registrations r
            WHERE
                    r.buildingid=%(building_id)s
            ;
            """
    params = {"building_id": building_id}
    return query_database(query, params)


def get_building_house_number(building_id):
    """
    Retrieves the house number for a given building ID.

    Args:
        building_id (int): The ID of the building.

    Returns:
        str or None: The house number if found, otherwise None.
    """

    house_number = get_building_house_number_from_database(building_id)
    if house_number:
        return house_number[0][0]
    else:
        logger.warning(
            "No street name received from db. nycdb.get_building_house_number is returning None"
        )
        return None
