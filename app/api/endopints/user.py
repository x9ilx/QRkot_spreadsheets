from fastapi import APIRouter

from app.core.user import auth_backend, fastapi_user
from app.schemas.user import UserCreate, UserRead, UserUpdate

router = APIRouter()
router.include_router(
    fastapi_user.get_auth_router(auth_backend),
    prefix='/auth/jwt',
    tags=['auth'],
)
router.include_router(
    fastapi_user.get_register_router(UserRead, UserCreate),
    prefix='/auth',
    tags=['auth'],
)
users_routers = fastapi_user.get_users_router(UserRead, UserUpdate)
users_routers.routes = [
    route
    for route in users_routers.routes
    if route.name != 'users:delete_user'
]
router.include_router(users_routers, prefix='/users', tags=['auth'])
