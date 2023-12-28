from typing import Callable, Tuple, Any, Dict
import requests
from src.server.database import models
import settings
import datetime

server_url = f'http://{settings.SERVER_HOST}:{settings.SERVER_PORT}'


def server_available(func) -> Callable[[tuple[Any, ...], dict[str, Any]], dict[str, str] | Any]:
    def need_it(*args, **kwargs):
        try:
            requests.get(url=server_url)
            return func(*args, **kwargs)
        except requests.exceptions.ConnectionError:
            return {'error': 'Server not available'}

    return need_it


# User
@server_available
def login(user_login: str, user_password: str) -> dict | None:
    answer = requests.post(
        url=f'{server_url}/user/login',
        data=f'{{"phone": "{user_login}", "password": "{user_password}"}}')

    return answer.json()


@server_available
def register(user: models.User) -> dict | int:
    data = f'{{"name": "{user.name}", "surname": "{user.surname}", "phone": "{user.phone}", "password": "{user.password}"}}'

    answer = requests.post(
        url=f'{server_url}/user/create',
        data=data)

    return answer.json()


@server_available
def update_user(user: models.User) -> None | dict:
    data = f'{"name": "{user.name}", "surname": "{user.surname}", "phone": "{user.phone}", "password": "{user.password}"}'

    answer = requests.put(
        url=f'{server_url}/user/update/{user.id}',
        data=data)

    return answer.json()


# Tour
@server_available
def get_all_tours() -> dict:
    return requests.get(url=f'{server_url}/tour/get_all').json()


@server_available
def get_tour_by_id(tour_id: int) -> dict:
    return requests.get(url=f'{server_url}/tour/get/{tour_id}').json()


@server_available
def update_tour(tour: models.Tour) -> None | dict:
    data = f'{{"country_id": "{tour.country_id}", "hours": "{tour.hours}", "price": "{tour.price}"}}'
    return requests.put(url=f'{server_url}/tour/update/{tour.id}', data=data).json()


@server_available
def create_tour(tour: models.Tour) -> models.Tour:
    data = f'{{"country_id": "{tour.country_id}", "hours": "{tour.hours}", "price": "{tour.price}"}}'
    return requests.post(url=f'{server_url}/tour/create', data=data).json()


@server_available
def delete_tour(tour_id: int) -> None | dict:
    return requests.delete(url=f'{server_url}/tour/delete/{tour_id}').json()


# Country
@server_available
def get_country_by_id(country_id: int) -> dict:
    return requests.get(url=f'{server_url}/country/get/{country_id}').json()


@server_available
def get_all_countries():
    return requests.get(url=f'{server_url}/country/get_all').json()


# Ticket
@server_available
def get_ticket_by_id(ticket_id: int) -> dict:
    return requests.get(url=f'{server_url}/ticket/get/{ticket_id}').json()


@server_available
def get_all_tickets() -> dict:
    return requests.get(url=f'{server_url}/ticket/get_all').json()


@server_available
def new_ticket(ticket: models.Ticket) -> dict:
    data = f'{{"tour_id": "{ticket.tour_id}", "date_start": "{ticket.date_start}", "date_end": "{ticket.date_end}", "user_id": "{ticket.user_id}"}}'

    answer = requests.post(
        url=f'{server_url}/ticket/create/',
        data=data
    ).json()

    return answer


def update_ticket(ticket: models.Ticket):
    tour = get_tour_by_id(ticket.tour_id)
    date_start = datetime.datetime.now()
    date_end = date_start + datetime.timedelta(hours=int(tour['hours']))

    data = f'{{"tour_id": "{ticket.tour_id}", "date_start": "{str(date_start)}", "date_end": "{str(date_end)}", "user_id": "{ticket.user_id}"}}'

    answer = requests.put(
        url=f'{server_url}/ticket/update/{ticket.id}',
        data=data
    ).json()

    return answer

@server_available
def delete_ticket(ticket_id: int) -> None | dict:
    return requests.delete(url=f'{server_url}/ticket/delete/{ticket_id}').json()
