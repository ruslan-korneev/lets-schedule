from fastapi import status
from httpx import AsyncClient

from src.core.config import settings
from src.modules.auth.google.const import GOOGLE_OAUTH_ENDPOINT
from src.modules.auth.google.dependencies import get_google_authorization_url
from src.modules.auth.google.dto import GoogleAuthUrlResponse
from src.modules.auth.google.utils import construct_url


def test_authorization_url_getter() -> None:
    redirect_uri = "http://localhost:8000/v1/auth/google/callback"
    params = {
        "response_type": "code",
        "client_id": settings.google.client_id,
        "redirect_uri": redirect_uri,
        "scope": "email profile https://www.googleapis.com/auth/calendar",
        "access_type": "offline",
        "prompt": "consent",
    }
    required_auth_url = construct_url(GOOGLE_OAUTH_ENDPOINT, params)
    authorization_url = get_google_authorization_url(redirect_uri=redirect_uri)
    assert str(authorization_url) == str(required_auth_url)


async def test_authorization_url_router(api_client: AsyncClient) -> None:
    path = "v1/auth/google/callback"
    base_url = str(settings.app_host).removesuffix("/")
    redirect_uri = f"{base_url}/{path}"
    params = {
        "response_type": "code",
        "client_id": settings.google.client_id,
        "redirect_uri": redirect_uri,
        "scope": "email profile https://www.googleapis.com/auth/calendar",
        "access_type": "offline",
        "prompt": "consent",
    }
    required_auth_url = construct_url(GOOGLE_OAUTH_ENDPOINT, params)
    response = await api_client.get("/v1/auth/google")
    assert response.status_code == status.HTTP_200_OK, response.json()
    data = GoogleAuthUrlResponse.model_validate(response.json())
    assert str(data.auth_url) == str(required_auth_url)
