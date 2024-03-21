from typing import List, Any, Sequence

from sqlalchemy import select, Row, RowMapping, and_, func
from sqlalchemy.ext.asyncio import AsyncSession
from collections import Counter

from src import config
from src.cars.models import CarModel, FuelModel, MaintenanceModel
from src.cars.schemas import CarsFiltersSchema
from src.auth.models import LogModel
from src.models import UserModel

LITERS_IN_GALON = 5.546


async def get_cars_makes(db_session: AsyncSession) -> Sequence[Row[Any] | RowMapping | Any]:
    return (await db_session.scalars(select(CarModel.make).group_by(CarModel.make))).all()


async def get_cars_models(db_session: AsyncSession, car_make: str) -> Sequence[Row[Any] | RowMapping | Any]:
    return (await db_session.scalars(
        select(CarModel.model).where(CarModel.make == car_make).group_by(CarModel.model))).all()


async def get_recommended_car(db_session: AsyncSession, user: UserModel):
    car_models = await (db_session.execute(select(
        CarModel
    ).where(
        and_(LogModel.user_id == user.id, LogModel.car_id == CarModel.id)
    )))
    favourite_class = Counter([car[0].class_prediction for car in car_models]).most_common(1)[0][0]
    filters = CarsFiltersSchema(min_price=0, max_price=9999999)
    cars = await get_cars(db_session, filters, favourite_class)
    return cars[0]


async def add_log(db_session: AsyncSession, user: UserModel, car: CarModel):
    log = LogModel(user_id=user.id, car_id=car.id)
    # user.logs.append(log)
    db_session.add(log)
    await db_session.commit()


async def filter_cars(filters: CarsFiltersSchema):
    stmt = []
    if isinstance(filters.min_price, int):
        stmt.append((CarModel.price >= filters.min_price))
    if isinstance(filters.max_price, int):
        stmt.append((CarModel.price <= filters.max_price))

    if isinstance(filters.make, List):
        stmt.append((CarModel.make.in_(filters.make)))
        if isinstance(filters.model, List):
            stmt.append((CarModel.model.in_(filters.model)))

    if isinstance(filters.year_min, int):
        stmt.append((CarModel.year >= filters.year_min))
    if isinstance(filters.year_max, int):
        stmt.append((CarModel.year <= filters.year_max))

    if isinstance(filters.engine_size_min, int):
        stmt.append((CarModel.engine_size >= filters.engine_size_min))
    if isinstance(filters.engine_size_max, int):
        stmt.append((CarModel.engine_size <= filters.engine_size_max))

    if isinstance(filters.mpg_min, int):
        stmt.append((CarModel.mpg >= filters.mpg_min))
    if isinstance(filters.mpg_max, int):
        stmt.append((CarModel.mpg <= filters.mpg_max))

    if isinstance(filters.tax_min, int):
        stmt.append((CarModel.tax >= filters.tax_min))
    if isinstance(filters.tax_max, int):
        stmt.append((CarModel.tax <= filters.tax_max))

    if isinstance(filters.fuel_type, List):
        stmt.append((CarModel.fuel_type.in_(filters.fuel_type)))

    if isinstance(filters.mileage_min, int):
        stmt.append((CarModel.mileage >= filters.mileage_min))
    if isinstance(filters.mileage_max, int):
        stmt.append((CarModel.mileage <= filters.mileage_max))

    if isinstance(filters.transmission, List):
        stmt.append((CarModel.fuel_type.in_(filters.transmission)))

    # return (await db_session.scalars(stmt.limit(15))).all()
    return stmt


async def get_cars(db_session: AsyncSession, filters: CarsFiltersSchema, class_: int = None):
    conditions = await filter_cars(filters)
    if class_ is not None:
        conditions.append((CarModel.class_prediction == class_))

    galons_spent_in_5years = config.EARLY_MILEAGE * 5 / CarModel.mpg
    liters_spent_in_5years = galons_spent_in_5years * LITERS_IN_GALON
    fuel_price_for_5years = liters_spent_in_5years * FuelModel.fuel_price_in_pounds
    other_payments_for_5years = (CarModel.tax + MaintenanceModel.maintenance_cost) * 5
    five_years_price = fuel_price_for_5years + other_payments_for_5years + CarModel.price

    stmt = select(CarModel,
                  (five_years_price).label(
                      'five_years_price'),
                  (galons_spent_in_5years).label(
                      'galons_spent_in_5years'),
                  (liters_spent_in_5years).label(
                      'liters_spent_in_5years'),
                  (fuel_price_for_5years).label(
                      'fuel_price_for_5years'),
                  (other_payments_for_5years).label(
                      'other_payments_for_5years')
                  ).where(and_(*conditions))

    # 5 - 100% of 5y price will be considered, 4 - 80% will be considered etc
    satisfaction_percents = 100 / (CarModel.satisfaction * (100 / config.MAX_SATISFACTION))

    return (await db_session.execute(
        stmt.join(FuelModel, CarModel.fuel_type == FuelModel.fuel_type).join(
            MaintenanceModel, (
                                      CarModel.make == MaintenanceModel.make
                              ) & (
                                      CarModel.model == MaintenanceModel.model
                              ) & (
                                      CarModel.year == MaintenanceModel.year
                              )
        # ))).all()
        ).order_by(five_years_price * satisfaction_percents).limit(3))).mappings().all()
