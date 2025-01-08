from fastapi import Depends, Request
from httpx import AsyncClient

from src.core.config import settings
from src.core.dependencies.http import get_httpx_client
from src.modules.auth.google.const import (
    GOOGLE_AUTH_CALLBACK_ROUTER_NAME,
    GOOGLE_OAUTH_ENDPOINT,
)
from src.modules.auth.google.dto import GoogleAuthToken
from src.modules.auth.google.utils import construct_url, destruct_url


def get_google_redirect_uri(request: Request) -> str:
    google_redirect_url = str(request.url_for(GOOGLE_AUTH_CALLBACK_ROUTER_NAME))
    deconstructed_url = destruct_url(google_redirect_url)
    base_url = str(settings.app_host).removesuffix("/")
    path = deconstructed_url.path.removeprefix("/")
    return f"{base_url}/{path}"


def get_google_authorization_url(redirect_uri: str = Depends(get_google_redirect_uri)) -> str:
    params = {
        "response_type": "code",
        "client_id": settings.google.client_id,
        "redirect_uri": redirect_uri,
        "scope": "email profile https://www.googleapis.com/auth/calendar",
        "access_type": "offline",
        "prompt": "consent",
    }
    return construct_url(GOOGLE_OAUTH_ENDPOINT, params)


async def get_google_auth_token(
    code: str,
    redirect_uri: str = Depends(get_google_redirect_uri),
    http_client: AsyncClient = Depends(get_httpx_client),
) -> GoogleAuthToken:
    response = await http_client.post(
        "https://oauth2.googleapis.com/token",
        data={
            "code": code,
            "client_id": settings.google.client_id,
            "client_secret": settings.google.client_secret,
            "redirect_uri": redirect_uri,
            "grant_type": "authorization_code",
        },
    )
    response.raise_for_status()
    return GoogleAuthToken.model_validate(response.json())
