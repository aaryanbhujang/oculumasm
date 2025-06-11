from ipaddress import ip_address
from urllib.parse import urlparse

def normalize_input(user_input: str) -> dict:
    """Identify input type and standardize format"""
    try:
        ip_address(user_input)
        return {"type": "ip", "target": user_input}
    except ValueError:
        if "." in user_input:  # Basic domain check
            return {"type": "domain", "target": user_input}
        raise ValueError("Invalid input - must be IP or domain")
        