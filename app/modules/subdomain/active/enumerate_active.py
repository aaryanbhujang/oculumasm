import time
import asyncio
from typing import AsyncGenerator
some_list = ["act1", "act2"]
async def act_enum(domain: str) -> AsyncGenerator[str, None]:
    for sub in some_list:
        fqdn = f"{sub}.{domain}"
        time.sleep(5)
        yield fqdn

