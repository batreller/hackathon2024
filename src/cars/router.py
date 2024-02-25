from fastapi import APIRouter, Depends, HTTPException

from src.auth import service
from src.auth.dependencies import CurrentUserDep
from src.auth.schemas import RegisterData, UserSchemeDetailed, LoginData, Token
from src.auth.exceptions import UserAlreadyExists
from src.cars.schemas import CarsFiltersSchema
from src.cars.service import get_cars_makes, get_cars_models, get_cars
from src.database import get_db_session, DBSessionDep
from src.exceptions import InvalidCredentials, TokenParseError
from src.models import UserModel

router = APIRouter()


@router.get("/makes")
async def get_makes(db_session: DBSessionDep):
    return await get_cars_makes(db_session)


@router.get("/models/{car_make}")
async def get_models(car_make: str, db_session: DBSessionDep):
    print(car_make, 'car_make')
    return await get_cars_models(db_session, car_make)


@router.post("/find")
async def find_cars(filters: CarsFiltersSchema,
                    db_session: DBSessionDep
                    ):
    car = await get_cars(db_session, filters)
    # await add_log()
    return car
