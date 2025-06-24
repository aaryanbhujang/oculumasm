import time
import asyncio
from typing import AsyncGenerator
some_list = ["pass1", "pass2", "pass3"]
async def pass_enum(domain: str) -> AsyncGenerator[str, None]:
    for sub in some_list:
        fqdn = f"{sub}.{domain}"
        time.sleep(5)
        yield fqdn

