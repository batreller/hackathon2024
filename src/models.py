from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship

from src.database import Base


class UserModel(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True)
    promotions = Column(Boolean)
    guest = Column(Boolean)
    password = Column(String)  # hash

    logs = relationship("LogModel", back_populates="user")


    def __repr__(self):
        return f"<UserModel(id='{self.id}', email='{self.email}')>"
