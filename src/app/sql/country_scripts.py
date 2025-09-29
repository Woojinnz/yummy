import psycopg
from app.dto.location import Country
from app.utils.config import load_config
from typing import List

def insert_single_country(country: Country) -> int | None:
    """ INSERT a single country into the COUNTRY table """

    sql = " INSERT INTO country (name, iso_code) VALUES (%s, %s) RETURNING id"

    country_id = None
    config = load_config()

    try:
        with psycopg.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(sql, (country.name, country.iso_code))
                rows = cur.fetchone()

                if rows:
                    country_id = rows[0]

                conn.commit()

    except (Exception, psycopg.DatabaseError) as error:
        print(error)
    finally:
        return country_id
    
def get_country_using_iso_code(iso_code: str) -> Country | None:
    """ 
    READ Country Dataclass using iso_code from the COUNTRY table 
    There should only be 1 matching row 
    """

    sql = """ SELECT * FROM country WHERE iso_code = %s """

    country = None
    config = load_config()

    try:
        with psycopg.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(sql, (iso_code,))
                rows = cur.fetchone()

                if rows:
                    country = Country(rows[0], rows[1], rows[2])

    except (Exception, psycopg.DatabaseError) as error:
        print(error)
    finally:
        return country

def get_countries_using_name(name: str) -> List[Country]:
    """ 
    READ all countries with %LIKE% name (matching the start)
    new = [ New Zealand, New Caledonia, etc..]
    """

    sql = """ SELECT * FROM country WHERE name ILIKE %s """

    countries = []
    config = load_config()

    try:
        with psycopg.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(sql, (f"{name}%",))
                rows = cur.fetchall()

                for country in rows:
                    countries.append(Country(country[0], country[1], country[2]))

    except (Exception, psycopg.DatabaseError) as error:
        print(error)
    finally:
        return countries


if __name__ == "__main__":
    country = Country(None, "New Zealand", "NZ")
    id = insert_single_country(country)
    if id:
        print(id)

    country = Country(None, "New Caledonia", "NC")
    id = insert_single_country(country)
    if id:
        print(id)

    print(get_country_using_iso_code("NZ"))
    print(get_countries_using_name('new'))