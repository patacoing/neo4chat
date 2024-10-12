from typing import Any

from app.configuration.database.async_driver import IAsyncDriver, AsyncDriver
from app.exceptions.database import DatabaseNotConnectedException


class Database:
    def __init__(self, uri: str, auth: tuple[str, str], async_driver: IAsyncDriver = AsyncDriver()) -> None:
        self.uri = uri
        self.auth = auth
        self.async_driver = async_driver
        self.connected = False

    def connect(self) -> None:
        self.async_driver.connect(self.uri, self.auth)
        self.connected = True

    async def close(self) -> None:
        if not self.connected:
            raise DatabaseNotConnectedException()

        await self.async_driver.close()
        self.connected = False

    async def query(self, query: str, **kwargs: Any) -> Any:
        if not self.connected:
            raise DatabaseNotConnectedException()

        return await self.async_driver.query(query, **kwargs)