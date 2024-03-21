from sqlalchemy import Integer, Column, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from src.database import Base
from sqlalchemy.sql import func


class LogModel(Base):
    __tablename__ = 'logs'

    id = Column(Integer, primary_key=True)

    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("UserModel", back_populates="logs")

    car_id = Column(Integer, ForeignKey('cars.id'))
    car = relationship("CarModel", back_populates="logs")

    timestamp = Column(DateTime, default=func.now())

    def __repr__(self):
        return f"<LogModel(id='{self.id}', user_id='{self.user_id}', car_id={self.car_id})>"
