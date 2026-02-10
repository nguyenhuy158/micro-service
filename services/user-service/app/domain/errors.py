class DomainError(Exception):
    pass


class UserNotFoundError(DomainError):
    pass


class UserAlreadyExistsError(DomainError):
    pass


class InvalidCredentialsError(DomainError):
    pass


class InactiveUserError(DomainError):
    pass


class InvalidGoogleTokenError(DomainError):
    pass


class TotpAlreadyEnabledError(DomainError):
    pass


class TotpSecretRequiredError(DomainError):
    pass


class InvalidTotpCodeError(DomainError):
    pass


class NoPasswordSetError(DomainError):
    pass


class IncorrectPasswordError(DomainError):
    pass
