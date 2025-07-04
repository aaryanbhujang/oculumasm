import httpx
from typing import AsyncGenerator

async def ct_log(target: str) -> AsyncGenerator[str, None]:
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/json"
    }

    timeout = httpx.Timeout(40.0, connect=25.0)  # increase total and connect timeouts

    async with httpx.AsyncClient(timeout=timeout) as client:
        try:
            resp = await client.get(
                f"https://crt.sh/?q={target}&output=json",
                headers=headers
            )
        except httpx.ReadTimeout:
            print("[X] Request timed out")
            return

        if resp.status_code != 200 or not resp.text.strip().startswith("["):
            print("[X] Invalid or blocked response from crt.sh")
            print(f"[DEBUG] Status: {resp.status_code}")
            print(f"[DEBUG] Response: {resp.text[:200]}")
            return

        try:
            for entry in resp.json():
                yield entry["name_value"]
        except Exception as e:
            print("[X] JSON parse failed")
            print(f"[DEBUG] Error: {e}")
            print(f"[DEBUG] Response: {resp.text[:200]}")
