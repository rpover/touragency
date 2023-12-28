from src.server.database.models import Ticket
from src.server.resolves.user import dbmanager


def get(ticket_id: int) -> Ticket | None:
    res = dbmanager.execute_query(
        query='select * from Ticket where id=(?)',
        args=(ticket_id,))

    return None if not res else Ticket(
        id=res[0],
        tour_id=res[1],
        date_start=res[2],
        date_end=res[3],
        user_id=res[4]
    )


def get_all() -> list[Ticket] | dict:
    ticket_list = dbmanager.execute_query(
        query="select * from Ticket",
        fetchone=False)

    res = []

    if ticket_list:
        for ticket in ticket_list:
            res.append(Ticket(
                id=ticket[0],
                tour_id=ticket[1],
                date_start=ticket[2],
                date_end=ticket[3],
                user_id=ticket[4]
            ))

    return res


def delete(ticket_id: int) -> None:
    return dbmanager.execute_query(
        query='delete from Ticket where id=(?)',
        args=(ticket_id,))


def create(new_ticket: Ticket) -> int | dict:
    res = dbmanager.execute_query(
        query="insert into Ticket (tourId, date_start, date_end, userId) values(?,?,?,?) returning id",
        args=(new_ticket.tour_id, new_ticket.date_start, new_ticket.date_end, new_ticket.user_id))

    if type(res) != dict:
        res = get(res[0])

    return res


def update(ticket_id: int, new_data: Ticket) -> None:
    return dbmanager.execute_query(
        query="update Ticket set (tourId, date_start, date_end, userId) = (?,?,?,?) where id=(?)",
        args=(new_data.tour_id, new_data.date_start, new_data.date_end, new_data.user_id, ticket_id))

