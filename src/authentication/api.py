from database.users.i_user_manager import IUserManager
from database.users.user import UserCreate, UserRead
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi_injector import Injected

from .i_authentication import IAuthentication
from .token import Token

router = APIRouter(prefix="/auth",
                   tags=["Authentication"],)


@router.post("/token", response_model=Token)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    authentication: IAuthentication = Injected(IAuthentication)
):
    try:
        token = authentication.login_user(
            form_data.username, form_data.password)
        return {"access_token": token, "token_type": "bearer"}
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )


@router.post(
    "/create-user",
    response_model=UserRead,
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_400_BAD_REQUEST: {
            "description": "User with that email already exists."
        }
    }
)
def create_user(user: UserCreate, user_manager: IUserManager = Injected(IUserManager)):
    try:
        new_user = user_manager.create_user(user)
        return new_user
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with that email already exists.",
        )
