from abc import ABC, abstractmethod


class TotpServicePort(ABC):
    @abstractmethod
    def generate_secret(self) -> str: ...

    @abstractmethod
    def get_uri(
        self, email: str, secret: str, issuer_name: str = "MicroShop"
    ) -> str: ...

    @abstractmethod
    def verify_code(self, secret: str, code: str) -> bool: ...
