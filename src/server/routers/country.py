import fastapi
from src.server.resolves import country
from src.server.database.models import Country

router = fastapi.APIRouter(prefix='/country', tags=['Country'])


@router.get('/get/{country_id}', response_model=Country | None)
def get(country_id: int) -> Country | None:
    return country.get(country_id)


@router.get('/get_all', response_model=list[Country] | dict)
def get_all() -> list[Country] | dict:
    return country.get_all()


@router.delete('/delete/{country_id}', response_model=None)
def remove(country_id: int) -> None:
    return country.delete(country_id)


@router.post('/create/', response_model=Country | dict)
def create(new_country: Country) -> Country | dict:
    return country.create(new_country)


@router.put("/update/{user_id}", response_model=None)
def update(country_id: int, new_data: Country):
    return country.update(country_id=country_id, new_data=new_data)
