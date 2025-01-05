from httpx import AsyncClient
from fastapi import status


async def test_client_health(api_client: AsyncClient) -> None:
    response = await api_client.get("v1/health")
    response.raise_for_status()
    assert response.status_code == status.HTTP_200_OK
