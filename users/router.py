from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Depends, APIRouter

from users.crud import get_current_active_user
from users.schemas import UserRead, UserCreate, Token
from users.crud import UserCRUD


router = APIRouter(
    prefix="/users",
    tags=["users"]
)


@router.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    token = await UserCRUD.get_token(form_data.username, form_data.password)
    return token


@router.get("/users/me/", response_model=UserRead)
async def read_users_me(
    current_user: Annotated[UserRead, Depends(get_current_active_user)],
):
    return current_user


@router.post("/register", response_model=UserRead)
async def register_user(user: UserCreate):
    user = await UserCRUD.register(user)
    return user
