import fastapi
from src.server.database.models import Tour
from src.server.resolves import tour

router = fastapi.APIRouter(prefix='/tour', tags=['Tour'])


@router.get('/get/{tour_id}', response_model=Tour | None)
def get(tour_id: int) -> Tour | None:
    return tour.get(tour_id)


@router.get('/get_all', response_model=list[Tour])
def get_all() -> list[Tour]:
    return tour.get_all()


@router.delete('/delete/{tour_id}', response_model=None)
def delete(tour_id: int) -> None:
    return tour.delete(tour_id)


@router.post('/create/', response_model=Tour | dict)
def create(new_tour: Tour) -> Tour | dict:
    return tour.create(new_tour)


@router.put("/update/{tour_id}", response_model=None)
def update(tour_id: int, new_data: Tour) -> None:
    return tour.update(tour_id, new_data)

