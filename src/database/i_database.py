from abc import ABC, abstractmethod

from sqlmodel import Session


class IDatabase(ABC):
    @abstractmethod
    def create_database(self) -> None:
        """Creates a database according to implementation
           specification."""

    def get_session(self) -> Session:
        """Returns a session used to query the database."""
