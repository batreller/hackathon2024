from typing import List, Any, Sequence

from sqlalchemy import select, Row, RowMapping, and_
from sqlalchemy.ext.asyncio import AsyncSession

from src import config
from src.cars.models import CarModel, FuelModel, MaintenanceModel
from src.cars.schemas import CarsFiltersSchema

LITERS_IN_GALON = 5.546


async def get_cars_makes(db_session: AsyncSession) -> Sequence[Row[Any] | RowMapping | Any]:
    return (await db_session.scalars(select(CarModel.make).group_by(CarModel.make))).all()


async def get_cars_models(db_session: AsyncSession, car_make: str) -> Sequence[Row[Any] | RowMapping | Any]:
    return (await db_session.scalars(
        select(CarModel.model).where(CarModel.make == car_make).group_by(CarModel.model))).all()


async def filter_cars(db_session: AsyncSession, filters: CarsFiltersSchema):
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


async def get_cars(db_session: AsyncSession, filters: CarsFiltersSchema):
    conditions = await filter_cars(db_session, filters)

    stmt = select(CarModel, ((config.EARLY_MILEAGE / CarModel.mpg * LITERS_IN_GALON * FuelModel.fuel_price_in_pounds + CarModel.tax + MaintenanceModel.maintenance_cost) * 5 + CarModel.price).label('five_years_price')).where(and_(*conditions))

    return (await db_session.execute(
        stmt.join(FuelModel, CarModel.fuel_type == FuelModel.fuel_type).join(
            MaintenanceModel, (CarModel.make == MaintenanceModel.make) & (CarModel.model == MaintenanceModel.model) & (
                        CarModel.year == MaintenanceModel.year)).order_by
        (config.EARLY_MILEAGE / CarModel.mpg * LITERS_IN_GALON * FuelModel.fuel_price_in_pounds + CarModel.tax + MaintenanceModel.maintenance_cost + (CarModel.satisfaction * config.SATISFACTION_MULTIPLIER)).limit(
            150))).mappings().all()
