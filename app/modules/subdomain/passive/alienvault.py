import httpx
from typing import AsyncGenerator
import logging
logger = logging.getLogger(__name__)
async def alienvault_agent(target: str) -> AsyncGenerator[str, None]:
    url = f"https://otx.alienvault.com/api/v1/indicators/domain/{target}/passive_dns"
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/json"
    }

    timeout = httpx.Timeout(40.0, connect=25.0)
    logger.info("\n\n\n\n---------------------------Stealing from ALIENVAULT----------------------------------")

    async with httpx.AsyncClient(timeout=timeout) as client:
        try:
            resp = await client.get(url, headers=headers)
        except httpx.ReadTimeout:
            print("[X] Alienvault request timed out")
            return

        if resp.status_code != 200 or not resp.text.strip().startswith("{"):
            print("[X] Invalid response from Alienvault")
            print(f"[DEBUG] Status: {resp.status_code}")
            print(f"[DEBUG] Response: {resp.text[:200]}")
            return

        try:
            data = resp.json()
            for entry in data.get("passive_dns", []):
                sub = entry.get("hostname")
                if sub and target in sub:
                    logger.info(f"\n\n[ALIENVAULT]: {sub}")
                    yield sub
        except Exception as e:
            print("[X] Alienvault JSON parse failed")
            print(f"[DEBUG] Error: {e}")
            print(f"[DEBUG] Response: {resp.text[:200]}")
