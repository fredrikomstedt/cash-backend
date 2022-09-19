from abc import ABC, abstractmethod


class IJwtEncoder(ABC):
    @abstractmethod
    def encode(self, data: dict) -> str:
        """Encodes the given data using a JWT method."""

    @abstractmethod
    def decode(self, encoded_data: str) -> dict:
        """Decodes the given data using a JWT method."""
