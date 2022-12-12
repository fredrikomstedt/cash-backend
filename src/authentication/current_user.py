from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from fastapi_injector import Injected

from src.authentication.i_authentication import IAuthentication
from src.common.exceptions import ObjectNotFoundError

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")


def get_current_user(
    token: str = Depends(oauth2_scheme),
    authentication: IAuthentication = Injected(IAuthentication)
):
    try:
        return authentication.authenticate_user(token)
    except ObjectNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User does not exist.",
        )
