import src.client.api.resolvers
from src.server.database.models import User


class Session:
    auth: bool = False
    user: User = User(
        id=0,
        name='',
        surname='',
        phone='',
        password='',
        power_level=0
    )
    error = None
    server_available: bool = False

    def login(self, user_login, user_password) -> None:
        answer: User | dict = src.client.api.resolvers.login(user_login, user_password)

        match answer:
            case {'error': error}:
                self.error = error

            case {'id': _}:
                self.user = User(
                    id=answer['id'],
                    name=answer['name'],
                    surname=answer['surname'],
                    phone=answer['phone'],
                    password=user_password,
                    power_level=answer['power_level']
                )
                self.auth = True

    def register(self, user: User) -> None:
        answer: User | dict = src.client.api.resolvers.register(user)

        match answer:
            case {'error': error}:
                self.error = error

            case {'id': _}:
                self.auth = True

    def update(self, user: User) -> None:
        answer: User | dict = src.client.api.resolvers.update_user(user)

        match answer:
            case {'error': error}:
                self.error = error
