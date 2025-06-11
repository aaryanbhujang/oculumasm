MODULES = {
    "subdomains": {
        "runner": "app.modules.subdomains.run.run",  # Full dotted path
        "requires": ["domain"],
        "description": "Subdomain enumeration",
        "is_active": True  # Enable/disable modules dynamically
    },
    "port_scan": {
        "runner": "app.modules.portscan.run.run", 
        "requires": ["ip", "domain"],
        "description": "TCP port scanning",
        "is_active": True
    }
}

def get_available_modules(input_type: str) -> list:
    """Get enabled modules that support the input type"""
    return [
        name for name, config in MODULES.items()
        if input_type in config["requires"] and config["is_active"]
    ]

def get_runner(module_name: str):
    """Dynamically import the runner function"""
    from importlib import import_module
    module_path, func_name = MODULES[module_name]["runner"].rsplit(".", 1)
    module = import_module(module_path)
    return getattr(module, func_name)