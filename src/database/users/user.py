import uuid

from pydantic import EmailStr, Extra
from sqlmodel import Field, SQLModel


class UserBase(SQLModel):
    first_name: str
    last_name: str
    email: EmailStr
    is_verified: bool = False


class UserRead(UserBase):
    id: uuid.UUID


class UserCreate(UserBase, extra=Extra.forbid):
    password: str


class UserUpdate(UserBase):
    password: str | None = None


class User(UserBase, table=True):
    internal_id: int | None = Field(default=None, primary_key=True)
    id: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        index=True,
        nullable=False,
    )
    hashed_password: str | None = None
