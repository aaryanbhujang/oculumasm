# from . import ct_logs, api_clients
# from typing import Set, Awaitable
# import asyncio

# async def run(domain: str) -> Set[str]:
#     """Run all passive enumeration methods"""
#     results = set()
#     tasks: List[Awaitable] = [
#         ct_logs.query(domain),
#         api_clients.check_virustotal(domain)
#     ]
    
#     for task in asyncio.as_completed(tasks):
#         try:
#             results.update(await task)
#         except Exception as e:
#             print(f"Passive scan failed: {e}")
            
#     return results