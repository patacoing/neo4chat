from abc import ABC
from typing import Any
from neo4j import AsyncGraphDatabase


class IAsyncDriver(ABC):
    def connect(self, uri: str, auth: tuple[str, str]) -> None:  # pragma: no cover
        ...

    async def close(self) -> None:  # pragma: no cover
        ...

    async def query(self, query: str, **kwargs: Any) -> Any:  # pragma: no cover
        ...


class AsyncDriver(IAsyncDriver):
    def connect(self, uri: str, auth: tuple[str, str]) -> None:
        self.driver = AsyncGraphDatabase.driver(
            uri,
            auth=auth
        )

    async def close(self) -> None:
        await self.driver.close()

    async def query(self, query: str, **kwargs: Any) -> Any:
        records, summary, keys = await self.driver.execute_query(query, **kwargs)

        if query.startswith("CREATE"):
            assert summary.counters.nodes_created > 0

        return records, summary, keys