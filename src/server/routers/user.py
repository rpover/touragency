import fastapi
from src.server.resolves import user
from src.server.database.models import User, UserAuth

router = fastapi.APIRouter(prefix='/user', tags=['User'])


@router.get('/get/{user_id}', response_model=User | None)
def get(user_id: int) -> User | None:
    return user.get(user_id)


@router.get('/get_all', response_model=list[User] | dict)
def get_all() -> list[User] | dict:
    return user.get_all()


@router.delete('/delete/{user_id}', response_model=None)
def delete(user_id: int) -> None:
    return user.delete(user_id)


@router.post('/create/', response_model=User | dict)
def create(new_user: User) -> User | dict:
    return user.create(new_user)


@router.put("/update/{user_id}", response_model=None)
def update(user_id: int, new_data: User) -> None:
    return user.update(user_id=user_id, new_data=new_data)


@router.post('/login', response_model=User | dict)
def login(user_auth: UserAuth) -> User | dict:
    return user.login(user_auth.phone, user_auth.password)

