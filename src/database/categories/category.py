from typing import TYPE_CHECKING

from pydantic import Extra
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from src.database.users.user import User


class CategoryBase(SQLModel):
    name: str


class CategoryRead(CategoryBase):
    pass


class CategoryCreate(CategoryBase, extra=Extra.forbid):
    pass


class CategoryUpdate(CategoryBase, extra=Extra.forbid):
    pass


class Category(CategoryBase, table=True):
    name: str = Field(primary_key=True)

    user_id: str = Field(foreign_key="user.id")
    user: "User" = Relationship(
        back_populates="categories", sa_relationship_kwargs={"lazy": "joined"}
    )
