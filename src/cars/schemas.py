from typing import Optional, List

from pydantic import BaseModel


class CarsFiltersSchema(BaseModel):
    make: Optional[List[str]] = None
    model: Optional[List[str]] = None

    year_min: Optional[int] = None
    year_max: Optional[int] = None

    engine_size_min: Optional[float] = None
    engine_size_max: Optional[float] = None

    mpg_min: Optional[float] = None
    mpg_max: Optional[float] = None

    tax_min: Optional[int] = None
    tax_max: Optional[int] = None

    fuel_type: Optional[List[str]] = None

    mileage_min: Optional[int] = None
    mileage_max: Optional[int] = None

    transmission: Optional[List[str]] = None

    min_price: int
    max_price: int
