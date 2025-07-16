import asyncio
from typing import AsyncGenerator, Callable, List, Union
from app.modules.subdomain.passive.ct_logs import ct_log
from app.modules.subdomain.passive.alienvault import alienvault_agent

PASSIVE_SOURCES: List[Callable[[str], AsyncGenerator[str, None]]] = [
    ct_log,
    alienvault_agent
]

async def pass_enum(domain: str) -> AsyncGenerator[Union[str, dict], None]:
    seen = set()
    queue = asyncio.Queue()

    async def collect_source(source: Callable[[str], AsyncGenerator[str, None]]):
        async for sub in source(domain):
            for splitted in sub.splitlines():
                sub_clean = splitted.strip()
                if sub_clean and sub_clean not in seen:
                    seen.add(sub_clean)
                    await queue.put(sub_clean)

    async def enqueue_all():
        tasks = [asyncio.create_task(collect_source(src)) for src in PASSIVE_SOURCES]
        await asyncio.gather(*tasks)
        await queue.put(None)  # Sentinel value to signal completion

    producer = asyncio.create_task(enqueue_all())

    while True:
        item = await queue.get()
        if item is None:
            break
        yield item

    await producer  # ensure all producers finish
