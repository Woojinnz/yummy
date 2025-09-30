from app.database.dto.location import Country
from app.database.utils.database import insert_single_sql, select_sql
from typing import List

def insert_single_country(country: Country) -> int | None:
    """ INSERT a single country into the COUNTRY table """

    sql = " INSERT INTO country (name, iso_code) VALUES (%s, %s) RETURNING id"
    values = (country.name, country.iso_code)
    return insert_single_sql(sql, values)

    
def get_country_using_iso_code(iso_code: str) -> List[Country]:
    """ 
    READ Country Dataclass using iso_code from the COUNTRY table 
    There should only be 1 matching row but still returns as a list
    """

    sql = """SELECT id, name, iso_code FROM country WHERE iso_code = %s"""
    values = (iso_code, )
    
    return select_sql(sql, values, Country)

def get_countries_using_name(name: str) -> List[Country]:
    """ 
    READ all countries with %LIKE% name (matching the start)
    new = [ New Zealand, New Caledonia, etc..]
    """

    sql = """SELECT id, name, iso_code FROM country WHERE name ILIKE %s"""
    values = (f"{name}%",)

    return select_sql(sql, values, Country)


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