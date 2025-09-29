import psycopg
from app.dto.location import Country
from app.utils.config import load_config

# CRUD
# CREATE
# READ
# UPDATE
# DELETE

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
    



if __name__ == "__main__":
    country = Country(None, "New Zealand", "NZ")
    id = insert_single_country(country)
    if id:
        print(id)