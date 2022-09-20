import uuid

from pydantic import EmailStr, Extra
from sqlmodel import Field, SQLModel


class UserBase(SQLModel):
    first_name: str | None = None
    last_name: str | None = None
    email: EmailStr


class UserRead(UserBase):
    id: uuid.UUID


class UserCreate(UserBase, extra=Extra.forbid):
    password: str


class UserUpdate(SQLModel):
    first_name: str | None = None
    last_name: str | None = None


class UserUpdatePassword(SQLModel):
    old_password: str
    new_password: str


class User(UserBase, table=True):
    internal_id: int | None = Field(default=None, primary_key=True)
    id: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        index=True,
        nullable=False,
    )
    hashed_password: str | None = None
