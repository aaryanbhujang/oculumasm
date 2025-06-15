from pydantic import BaseModel, Field
from typing import List
from datetime import datetime

class SubdomainResult(BaseModel):
    domain: str = Field(..., description="The target domain that was scanned")
    subdomains: List[str] = Field(default_factory=list, description="List of discovered subdomains")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Scan completion timestamp")
    scan_type: str = Field(default="full", description="Type of scan performed (e.g., full, passive, active)")
    tool_used: str = Field(default="subfinder", description="Tool used for subdomain enumeration")
