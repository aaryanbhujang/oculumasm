import time
import asyncio
from typing import AsyncGenerator, Union
from app.modules.subdomain.passive.ct_logs import ct_log
#print(dir(app.modules.subdomain.passive.ct_logs))
async def pass_enum(domain: str) -> AsyncGenerator[Union[str, dict], None]:
    async for sub in ct_log(domain):
        for splittedsubs in sub.split("\n"):
            yield splittedsubs.strip()
'''
some_list = ["pass1", "pass2", "pass3"]
async def pass_enum(domain: str) -> AsyncGenerator[str, None]:
    for sub in some_list:
        fqdn = f"{sub}.{domain}"
        time.sleep(5)
        yield fqdn
'''
