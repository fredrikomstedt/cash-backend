from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_injector import Injected

from authentication.i_password_handler import IPasswordHandler
from common.exceptions import ObjectNotFoundError
from database.users.i_user_manager import IUserManager
from database.users.user import (User, UserCreate, UserRead, UserUpdate,
                                 UserUpdatePassword)

from .current_user import get_current_user
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


@router.patch(
    "/update-user",
    response_model=UserRead,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "User does not exist."
        }
    }
)
def update_user(
    user: UserUpdate,
    user_manager: IUserManager = Injected(IUserManager),
    current_user: User = Depends(get_current_user)
):
    try:
        updated_user = user_manager.update_user(current_user.id, user)
        return updated_user
    except ObjectNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User does not exist.",
        )


@router.patch(
    "/update-user-password",
    response_model=UserRead,
    responses={
        status.HTTP_400_BAD_REQUEST: {
            "description": "Old password is incorrect."
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "User does not exist."
        }
    }
)
def update_user_password(
    passwords: UserUpdatePassword,
    password_handler: IPasswordHandler = Injected(IPasswordHandler),
    user_manager: IUserManager = Injected(IUserManager),
    current_user: User = Depends(get_current_user)
):
    if not password_handler.verify_password(passwords.old_password, current_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Old password is incorrect.",
        )
    try:
        updated_user = user_manager.update_user_password(
            current_user.id, passwords.new_password)
        return updated_user
    except ObjectNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User does not exist.",
        )


@router.get(
    "/get-user",
    status_code=status.HTTP_200_OK,
    response_model=UserRead,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "User does not exist."
        }
    }
)
def get_user(
    current_user: User = Depends(get_current_user)
):
    return current_user


@router.delete(
    "/delete-user",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "User does not exist."
        }
    }
)
def delete_user(
    user_manager: IUserManager = Injected(IUserManager),
    current_user: User = Depends(get_current_user)
):
    try:
        user_manager.delete_user(current_user.id)
    except ObjectNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User does not exist.",
        )
