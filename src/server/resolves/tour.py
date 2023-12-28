from src.server.database.models import Tour
from src.server.resolves.user import dbmanager


def get(tour_id: int) -> Tour | None:
    res = dbmanager.execute_query(
        query='select * from Tour where id=(?)',
        args=(tour_id,))

    return None if not res else Tour(
        id=res[0],
        country_id=res[1],
        hours=res[2],
        price=res[3]
    )


def get_all() -> list[Tour] | dict:
    tour_list = dbmanager.execute_query(
        query="select * from Tour",
        fetchone=False)

    res = []

    if tour_list:
        for tour in tour_list:
            res.append(Tour(
                id=tour[0],
                country_id=tour[1],
                hours=tour[2],
                price=tour[3]
            ))

    return res


def delete(tour_id: int) -> None:
    return dbmanager.execute_query(
        query='delete from Tour where id=(?)',
        args=(tour_id,))


def create(new_tour: Tour) -> int | dict:
    res = dbmanager.execute_query(
        query="insert into Tour (countryId, hours, price) values(?,?,?) returning id",
        args=(new_tour.country_id, new_tour.hours, new_tour.price))

    if type(res) != dict:
        res = get(res[0])

    return res


def update(tour_id: int, new_data: Tour) -> None:
    return dbmanager.execute_query(
        query="update Tour set (countryId, hours, price) = (?,?,?) where id=(?)",
        args=(new_data.country_id, new_data.hours, new_data.price, tour_id))

