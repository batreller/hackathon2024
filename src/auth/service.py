from datetime import datetime, timedelta
from typing import Optional

import jwt
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from jose import JWTError
from src.auth import models, schemas
from src.auth.exceptions import UserDoesntExist, InvalidPassword
from src.auth.schemas import RegisterData, LoginData
from src.database import get_db_session
from src.exceptions import InvalidCredentials
from src.models import UserModel
from src import config
from passlib.context import CryptContext
from typing import Annotated

oauth2_bearer = OAuth2PasswordBearer(
    tokenUrl="auth/login",
    scheme_name="JWT"
)


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    """
    Verify if the provided plain text password matches the hashed password.
    """
    return pwd_context.verify(plain_password, hashed_password)


async def user_exists(db_session: AsyncSession, email: str) -> bool:
    user = (await db_session.execute(select(UserModel).where(UserModel.email == email))).scalar()
    return user is not None


async def validate_user(db_session: AsyncSession, email: str, password: str) -> str:
    user = await get_user_by_email(db_session, email)
    if verify_password(password, user.password):
        return create_access_token(user.id)
    else:
        raise InvalidPassword()


async def get_user_by_id(db_session: AsyncSession, user_id: int) -> UserModel:
    user = (await db_session.scalars(select(UserModel).where(UserModel.id == user_id))).first()
    if not user:
        raise UserDoesntExist()
    return user


async def get_user_by_email(db_session: AsyncSession, user_email: str) -> UserModel:
    user = (await db_session.scalars(select(UserModel).where(UserModel.email == user_email))).first()
    if not user:
        raise UserDoesntExist()
    return user


def create_access_token(user_id: int) -> str:
    to_encode = {"sub": user_id}
    expire = datetime.utcnow() + timedelta(minutes=config.JWT_EXPIRY_TIME)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, config.SECRET_KEY, algorithm=config.JWT_ALGORITHM)
    return encoded_jwt


async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)], db_session: AsyncSession = Depends(get_db_session), fatal: bool = False) -> UserModel:
    try:
        payload = jwt.decode(token, config.SECRET_KEY, algorithms=[config.JWT_ALGORITHM])
        user_id = int(payload.get("sub"))  # todo add exception for this
        if user_id is None:
            raise InvalidCredentials()
    except JWTError:
        raise InvalidCredentials()
    user = await get_user_by_id(db_session, user_id)
    # todo prob dont need that expcetion cuz get_user_by_id will cause exception if it needs to
    if user is None:
        raise InvalidCredentials()
    return user


async def create_user(db_session: AsyncSession, register_data: RegisterData) -> UserModel:
    db_user = UserModel(email=register_data.email, password=pwd_context.hash(register_data.password),
                        promotions=register_data.promotions)
    db_session.add(db_user)
    await db_session.commit()
    await db_session.refresh(db_user)
    return db_user
