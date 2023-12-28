from src.server.database.models import Country
from src.server.resolves.user import dbmanager


def get(country_id: int) -> Country | None:
    res = dbmanager.execute_query(
        query='select * from Country where id=(?)',
        args=(country_id,))

    return None if not res else Country(
        id=res[0],
        name=res[1]
    )


def get_all() -> list[Country] | dict:
    country_list = dbmanager.execute_query(
        query="select * from Country",
        fetchone=False)

    res = []

    if country_list:
        for user in country_list:
            res.append(Country(
                id=user[0],
                name=user[1],
            ))

    return res


def delete(country_id: int) -> None:
    return dbmanager.execute_query(
        query='delete from Country where id=(?)',
        args=(country_id,))


def create(new_country: Country) -> int | dict:
    res = dbmanager.execute_query(
        query="insert into Country (name) values(?) returning id",
        args=(new_country.name,))

    if type(res) != dict:
        res = get(res[0])

    return res


def update(country_id: int, new_data: Country) -> None:
    return dbmanager.execute_query(
        query="update Country set (name) = (?) where id=(?)",
        args=(new_data.name, country_id))
