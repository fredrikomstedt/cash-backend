from abc import ABC, abstractmethod


class IDatabaseDeleter(ABC):
    @abstractmethod
    def delete_database(self) -> None:
        """Deletes a previously created database.
        This should only be used for test purposes."""
