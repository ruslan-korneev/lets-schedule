from httpx import AsyncClient


async def test_client_health(api_client: AsyncClient) -> None:
    await api_client.get("health")
