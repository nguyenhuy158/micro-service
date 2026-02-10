import pyotp

from app.domain.ports.totp_service import TotpServicePort


class PyotpTotpService(TotpServicePort):
    def generate_secret(self) -> str:
        return pyotp.random_base32()

    def get_uri(self, email: str, secret: str, issuer_name: str = "MicroShop") -> str:
        return pyotp.totp.TOTP(secret).provisioning_uri(
            name=email, issuer_name=issuer_name
        )

    def verify_code(self, secret: str, code: str) -> bool:
        totp = pyotp.totp.TOTP(secret)
        return totp.verify(code)
