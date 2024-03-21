from fastapi import APIRouter

from src.auth.dependencies import CurrentUserDep
from src.auth.schemas import RegisterData, LoginData, Token, UserScheme
from src.auth.exceptions import UserAlreadyExists
from src import config
from src.auth import service
from src.database import DBSessionDep
from src.exceptions import InvalidCredentials

router = APIRouter()


@router.post(
    "/login",
    response_model=Token
)
async def login(
        login_data: LoginData,
        db_session: DBSessionDep
) -> Token:
    if login_data.email is None or login_data.password is None:
        raise InvalidCredentials()

    jwt_token = await service.validate_user(db_session, login_data.email, login_data.password)
    return Token(access_token=jwt_token, token_type="Bearer")


@router.post(
    "/register",
    response_model=Token
)
async def register(
        register_data: RegisterData,
        db_session: DBSessionDep
):
    if register_data.email is None or register_data.password is None:
        raise InvalidCredentials()

    if await service.user_exists(db_session, register_data.email):
        raise UserAlreadyExists()

    user_model = await service.create_user(db_session, register_data)
    jwt_token = await service.validate_user(db_session, register_data.email, register_data.password)
    return Token(access_token=jwt_token, token_type="Bearer")


@router.get(
    "/me",
    response_model=UserScheme
)
async def get_me(
        user: CurrentUserDep
):
    return UserScheme.from_orm(user)


@router.post(
    "/guest",
    response_model=Token
)
async def get_me(
        db_session: DBSessionDep
):
    user_model = await service.create_guest_user(db_session)
    jwt_token = service.create_access_token(user_model.id, expiry_time=config.GUEST_JWT_EXPIRY_TIME)
    return Token(access_token=jwt_token, token_type="Bearer")
