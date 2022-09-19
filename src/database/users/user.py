import uuid

from pydantic import EmailStr, Extra
from sqlmodel import Field, SQLModel


class UserBase(SQLModel):
    first_name: str | None = None
    last_name: str | None = None
    email: EmailStr


class UserRead(UserBase):
    id: uuid.UUID
    is_verified: bool


class UserCreate(UserBase, extra=Extra.forbid):
    password: str


class UserUpdate(UserBase):
    password: str | None = None
    is_verified: bool | None = None


class User(UserBase, table=True):
    internal_id: int | None = Field(default=None, primary_key=True)
    id: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        index=True,
        nullable=False,
    )
    hashed_password: str | None = None
    is_verified: bool = False
