import urllib.parse
from typing import Any

from pydantic import field_validator
from pydantic_core import Url

from src.core.types.dto import BaseDTO


class GoogleAuthUrlResponse(BaseDTO):
    auth_url: Url

    @field_validator("auth_url", mode="before")
    @classmethod
    def validate_auth_url(cls, value: str) -> Url:
        value = str(value)
        try:
            url = Url(value)
        except ValueError:
            encoded_value = urllib.parse.quote_plus(value, safe=":/?=&")
            url = Url(encoded_value)

        return url


class URLComponentsDTO(BaseDTO):
    scheme: str
    netloc: str
    path: str
    params: str
    query: dict[str, Any]
    fragment: str


class GoogleAuthToken(BaseDTO):
    access_token: str
    refresh_token: str


class JWTResponse(BaseDTO):
    access_token: str
