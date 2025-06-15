from . import active, passive
from .schemas import SubdomainResult
from typing import List, Optional
import asyncio

class SubdomainScanner:
    def __init__(self, domain: str):
        self.domain = domain
        self.found = set()

    async def run(self, scan_type: str = "full") -> SubdomainResult:
        """Main execution flow"""
        # Passive always runs
        self.found.update(await passive.run(self.domain))
        
        if scan_type == "full":
            self.found.update(await active.run(self.domain))
            
        return SubdomainResult(
            domain=self.domain,
            subdomains=list(self.found),
            scan_type=scan_type
        )

# async def run(domain: str) -> SubdomainResult:
#     """Public interface"""
#     return await SubdomainScanner(domain).run()
import asyncio
from app.modules.subdomain.schemas import SubdomainResult

async def run(domain: str) -> SubdomainResult:
    """Dummy subdomain scanner for testing Celery with simulated delay"""
    
    await asyncio.sleep(15)  # Simulate 5 seconds of work
    
    return SubdomainResult(
        domain=domain,
        subdomains=[f"test1.{domain}", f"test2.{domain}"],
        scan_type="full"
    )
