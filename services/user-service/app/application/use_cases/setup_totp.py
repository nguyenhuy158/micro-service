from app.domain.ports.totp_service import TotpServicePort


class SetupTotpUseCase:
    def __init__(self, totp_service: TotpServicePort) -> None:
        self._totp_service = totp_service

    def execute(self, email: str) -> dict[str, str]:
        secret = self._totp_service.generate_secret()
        uri = self._totp_service.get_uri(email=email, secret=secret)
        return {"secret": secret, "otpauth_url": uri}
