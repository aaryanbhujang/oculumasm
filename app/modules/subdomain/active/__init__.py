# from . import dns_bruteforce, reverse_lookup
# from typing import Set, Awaitable
# import asyncio

# async def run(domain: str) -> Set[str]:
#     """Run all active enumeration methods"""
#     results = set()
#     tasks: List[Awaitable] = [
#         dns_bruteforce.run(domain),
#         reverse_lookup.run(domain)
#     ]
    
#     for task in asyncio.as_completed(tasks):
#         try:
#             results.update(await task)
#         except Exception as e:
#             print(f"Active scan failed: {e}")
            
#     return results