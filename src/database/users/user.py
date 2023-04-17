from typing import TYPE_CHECKING

from pydantic import EmailStr, Extra
from sqlmodel import Field, Relationship, SQLModel

from src.common.utils import str_uuid4

if TYPE_CHECKING:
    from src.database.categories.category import Category


class UserBase(SQLModel):
    first_name: str | None = None
    last_name: str | None = None
    email: EmailStr


class UserRead(UserBase):
    id: str


class UserCreate(UserBase, extra=Extra.forbid):
    password: str


class UserUpdate(SQLModel):
    first_name: str | None = None
    last_name: str | None = None


class UserUpdatePassword(SQLModel):
    old_password: str
    new_password: str


class User(UserBase, table=True):
    id: str = Field(
        default_factory=str_uuid4, index=True, nullable=False, primary_key=True
    )
    hashed_password: str | None = None

    categories: list["Category"] = Relationship(
        back_populates="user",
        sa_relationship_kwargs={"lazy": "selectin", "cascade": "delete"},
    )
