from app.infrastructure.clients.google_auth import HttpxGoogleAuthClient

_client = HttpxGoogleAuthClient()


async def verify_google_token(token: str) -> dict:
    return await _client.verify_token(token)
