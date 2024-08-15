from fastapi_users import schemas


class UserRead(schemas.BaseUser[int]):
    ...


class UserUpdate(schemas.BaseUserUpdate):
    ...


class UserCreate(schemas.BaseUserCreate):
    ...
