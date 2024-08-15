from typing import Union

from fastapi import Depends
from fastapi_users import (BaseUserManager, FastAPIUsers, IntegerIDMixin,
                           InvalidPasswordException)
from fastapi_users.authentication import (AuthenticationBackend,
                                          BearerTransport, JWTStrategy)
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.db import get_async_session
from app.models.user import User
from app.schemas.user import UserCreate


SECRET_KEY_LIFETIME = 3600
PASSWORD_MIN_LENGTH = 3


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)


async def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(
        secret=settings.secret,
        lifetime_seconds=SECRET_KEY_LIFETIME
    )


async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)


bearer_transport = BearerTransport(tokenUrl='auth/jwt/login')
auth_backend = AuthenticationBackend(
    name='jwt', transport=bearer_transport, get_strategy=get_jwt_strategy
)
fastapi_user = FastAPIUsers[User, int](get_user_manager, [auth_backend])
current_user = fastapi_user.current_user(active=True)
current_superuser = fastapi_user.current_user(active=True, superuser=True)


class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    async def validate_password(
        self, password: str, user: Union[UserCreate, User]
    ) -> None:
        if len(password) < PASSWORD_MIN_LENGTH:
            raise InvalidPasswordException(
                'Пароль должен быть длиннее 3 символов'
            )
        if user.email in password:
            raise InvalidPasswordException(
                'Пароль не должен включать электронную почту'
            )
