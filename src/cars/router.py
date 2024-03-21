from fastapi import APIRouter

from src.cars.schemas import CarsFiltersSchema
from src.cars.service import get_cars_makes, get_cars_models, get_cars, add_log, get_recommended_car
from src.auth.dependencies import CurrentUserDep
from src.database import DBSessionDep

router = APIRouter()


@router.get("/makes")
async def get_makes(db_session: DBSessionDep):
    return await get_cars_makes(db_session)


@router.get("/models/{car_make}")
async def get_models(car_make: str, db_session: DBSessionDep):
    print(car_make, 'car_make')
    return await get_cars_models(db_session, car_make)


@router.post("/find")
async def find_cars(
        user: CurrentUserDep,
        filters: CarsFiltersSchema,
        db_session: DBSessionDep
):
    cars = await get_cars(db_session, filters)

    for car in cars:
        await add_log(db_session, user, car.CarModel)
    return cars


@router.get("/recommended")
async def recommended_car(
        user: CurrentUserDep,
        db_session: DBSessionDep
):
    return await get_recommended_car(db_session, user)
