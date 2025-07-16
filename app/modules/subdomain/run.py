from typing import AsyncGenerator, Union
from app.modules.subdomain.passive.enumerate_passive import pass_enum
from app.modules.subdomain.active.enumerate_active import act_enum
from app.modules.subdomain.schemas import SubdomainResult

async def run(domain: str) -> AsyncGenerator[Union[str, dict], None]:
    """
    Streams each discovered subdomain and stage markers, all JSON-serializable.
    Yields:
      - str: each subdomain as it’s found
      - dict: {'stage': 'passive-start'}
      - dict: {'stage': 'active-start'}
      - dict: {'stage': 'done', 'result': <plain dict>}
    """
    result = SubdomainResult(domain=domain, subdomains=[])
    seen = set()

    # 1) Passive enumeration: tell client we're starting
    yield {"stage": "passive-start"}

    # stream each passive subdomain
    async for sub in pass_enum(domain):
        if "@" not in sub and sub not in seen:      # must be AsyncGenerator[str, None]
            seen.add(sub)
            result.subdomains.append(sub)
            yield sub

    # 2) Active enumeration
    yield {"stage": "active-start"}

    async for sub in act_enum(domain):       # must be AsyncGenerator[str, None]
        if sub not in seen:
            seen.add(sub)
            result.subdomains.append(sub)
            yield sub

    # 3) Done: hand back the full result as a plain dict
    yield {
        "stage":  "done",
        "result": result.dict()             # .dict() makes it JSON-serializable
    }