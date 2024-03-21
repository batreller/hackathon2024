from sqlalchemy import Integer, Column, Boolean, String, Float, ForeignKeyConstraint, select, and_, ForeignKey
from sqlalchemy.orm import relationship

from src.database import Base


class CarModel(Base):
    __tablename__ = 'cars'

    id = Column(Integer, primary_key=True)
    logs = relationship("LogModel", back_populates="car")

    make = Column(String)
    model = Column(String)
    year = Column(Integer)
    price = Column(Integer)
    transmission = Column(String)
    mileage = Column(Integer)
    fuel_type = Column(String)
    tax = Column(Integer)
    mpg = Column(Float)
    engine_size = Column(Float)
    satisfaction = Column(Float)
    class_prediction = Column(Integer)

    @property
    def maintenance(self):
        return (
            select(MaintenanceModel)
            .where(
                and_(
                    MaintenanceModel.make == self.make,
                    MaintenanceModel.model == self.model,
                    MaintenanceModel.year == self.year
                )
            )
        )

    def __repr__(self):
        return f"<CarModel(id='{self.id}', make='{self.make}', model={self.model})>"


class MaintenanceModel(Base):
    __tablename__ = 'maintenance'

    id = Column(Integer, primary_key=True)
    make = Column(String)
    model = Column(String)
    year = Column(Integer)
    maintenance_cost = Column(Float)


    def __repr__(self):
        return f"<MaintenanceModel(id='{self.id}', make='{self.make}', model={self.model})>"


class FuelModel(Base):
    __tablename__ = 'fuel'

    id = Column(Integer, primary_key=True)
    fuel_type = Column(String, unique=True)
    fuel_price_in_pounds = Column(Float)

    def __repr__(self):
        return f"<FuelModel(id='{self.id}', fuel_type='{self.fuel_type}', fuel_price_in_pounds={self.fuel_price_in_pounds})>"
