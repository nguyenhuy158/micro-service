from app.infrastructure.security.jwt_service import JoseJwtService
from app.infrastructure.security.password_hasher import BcryptPasswordHasher

_hasher = BcryptPasswordHasher()
_jwt_service = JoseJwtService()


def create_access_token(subject, expires_delta=None):
    return _jwt_service.create_access_token(subject, expires_delta)


def verify_password(plain_password, hashed_password):
    return _hasher.verify(plain_password, hashed_password)


def get_password_hash(password):
    return _hasher.hash(password)
