from typing import Optional

from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str  # todo maybe make it Literal


class RegisterData(BaseModel):
    email: str
    password: str
    promotions: bool


class LoginData(BaseModel):
    email: str
    password: str


class UserScheme(BaseModel):
    id: int
    email: Optional[str]
    promotions: Optional[bool]
    guest: Optional[bool]

    class Config:
        from_attributes = True


class UserSchemeDetailed(BaseModel):
    id: int
    email: Optional[str]
    promotions: Optional[bool]
    guest: Optional[bool]
    password: Optional[str]

    class Config:
        from_attributes = True
    #     underscore_attrs_are_private = True
    # todo make sure its ok
