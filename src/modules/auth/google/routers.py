from datetime import UTC, datetime

from fastapi import APIRouter, Depends, HTTPException, status
from httpx import AsyncClient
from jose import jwt
from pydantic_core import Url

from src.core.config import settings
from src.core.dependencies.http import get_httpx_client
from src.modules.auth.google.const import GOOGLE_AUTH_CALLBACK_ROUTER_NAME
from src.modules.auth.google.dependencies import (
    get_google_auth_token,
    get_google_authorization_url,
)
from src.modules.auth.google.dto import (
    GoogleAuthToken,
    GoogleAuthUrlResponse,
    JWTResponse,
)

router = APIRouter(prefix="/google")


@router.get("")
def get_google_auth_url(google_auth_url: Url = Depends(get_google_authorization_url)) -> GoogleAuthUrlResponse:
    return GoogleAuthUrlResponse(auth_url=google_auth_url)


@router.get("/callback", name=GOOGLE_AUTH_CALLBACK_ROUTER_NAME)
async def google_callback(
    google_auth_token: GoogleAuthToken = Depends(get_google_auth_token),
    http_client: AsyncClient = Depends(get_httpx_client),
) -> JWTResponse:
    user_info_response = await http_client.get(
        "https://www.googleapis.com/oauth2/v2/userinfo",
        headers={"Authorization": f"Bearer {google_auth_token.access_token}"},
    )

    _ = google_auth_token.refresh_token

    user_info = user_info_response.json()
    if "email" not in user_info:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Failed to retrieve user info")

    user_info["exp"] = datetime.now(tz=UTC) + settings.jwt.access_token_lifetime

    user_jwt = jwt.encode(user_info, settings.jwt.secret_key, algorithm=settings.jwt.algorithm)
    return JWTResponse(access_token=user_jwt)
