from httpx import AsyncClient

from src.core.http import AsyncClientSingleton


def get_httpx_client() -> AsyncClient:
    return AsyncClientSingleton()
